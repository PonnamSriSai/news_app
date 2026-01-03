import os
import hashlib
import uuid
from werkzeug.utils import secure_filename
from datetime import datetime
import mimetypes

class FileHandler:
    """Handles secure file uploads and management for reporter dashboard"""
    
        
    def __init__(self, upload_folder='static'):
        self.upload_folder = upload_folder
        self.images_folder = os.path.join(upload_folder, 'images')
        self.videos_folder = os.path.join(upload_folder, 'videos')
        
        # Create upload directories if they don't exist
        os.makedirs(self.images_folder, exist_ok=True)
        os.makedirs(self.videos_folder, exist_ok=True)
    
    def generate_unique_filename(self, original_filename, prefix=''):
        """Generate a unique filename to prevent conflicts"""
        # Get file extension
        name, ext = os.path.splitext(original_filename)
        
        # Create unique identifier using timestamp and UUID
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = str(uuid.uuid4())[:8]
        
        # Create secure filename
        secure_name = secure_filename(name)
        unique_filename = f"{prefix}{timestamp}_{unique_id}_{secure_name}{ext}"
        
        return unique_filename
    
    def save_uploaded_file(self, file_storage, file_type='image'):
        """Save uploaded file with security validations"""
        if not file_storage:
            return None, "No file provided"
        
        # Validate file type
        allowed_extensions = {
            'image': ['.jpg', '.jpeg', '.png', '.gif', '.webp'],
            'video': ['.mp4', '.mov', '.avi', '.mkv', '.webm']
        }
        
        original_filename = file_storage.filename
        file_ext = os.path.splitext(original_filename)[1].lower()
        
        if file_type not in allowed_extensions:
            return None, f"Invalid file type: {file_type}"
        
        if file_ext not in allowed_extensions[file_type]:
            return None, f"File extension {file_ext} not allowed for {file_type}s"
        
        # Generate unique filename
        prefix = 'img_' if file_type == 'image' else 'vid_'
        unique_filename = self.generate_unique_filename(original_filename, prefix)
        
        # Determine target folder
        target_folder = self.images_folder if file_type == 'image' else self.videos_folder
        target_path = os.path.join(target_folder, unique_filename)
        
        try:
            # Save file
            file_storage.save(target_path)
            
            # Get file size
            file_size = os.path.getsize(target_path)
            
            # Validate file size (10MB for images, 100MB for videos)
            max_size = 10 * 1024 * 1024 if file_type == 'image' else 100 * 1024 * 1024
            if file_size > max_size:
                os.remove(target_path)  # Remove oversized file
                return None, f"File too large. Max size: {max_size // (1024*1024)}MB"
            
            # Return relative path for database storage
            relative_path = f"static/{file_type}s/{unique_filename}"
            return relative_path, None
            
        except Exception as e:
            return None, f"Error saving file: {str(e)}"
    
    def get_file_url(self, relative_path):
        """Get the URL for a stored file"""
        if not relative_path:
            return None
        # Remove 'static/' prefix to get the correct URL path
        url_path = relative_path.replace('static/', '')
        return f"/{url_path}"
    
    def validate_file_content(self, file_storage):
        """Validate file content using MIME type detection"""
        # Read file signature to verify it's actually the claimed type
        file_signature = file_storage.stream.read(20)
        file_storage.stream.seek(0)  # Reset stream position
        
        # Simple MIME type validation based on signatures
        if file_signature.startswith(b'\xff\xd8\xff'):
            return 'image/jpeg'
        elif file_signature.startswith(b'\x89PNG'):
            return 'image/png'
        elif file_signature.startswith(b'GIF'):
            return 'image/gif'
        elif file_signature.startswith(b'RIFF') and b'WEBP' in file_signature[:12]:
            return 'image/webp'
        elif file_signature.startswith(b'\x00\x00\x00') and b'ftyp' in file_signature[:12]:
            return 'video/mp4'
        else:
            return 'application/octet-stream'  # Unknown type
