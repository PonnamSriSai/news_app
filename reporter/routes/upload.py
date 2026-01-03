from flask import request, jsonify, session, flash, redirect, url_for
from .. import reporter_bp
from ..utils.file_handler import FileHandler
from ..utils.validator import InputValidator
from werkzeug.utils import secure_filename

@reporter_bp.route('/upload/images', methods=['POST'])
def upload_images():
    """Handle image file uploads"""
    # Check authentication
    session_valid, session_message = InputValidator.validate_user_session(session)
    if not session_valid:
        return jsonify({'success': False, 'error': session_message}), 401
    
    if request.method != 'POST':
        return jsonify({'success': False, 'error': 'Method not allowed'}), 405
    
    try:
        # Check if files are present
        if 'files' not in request.files:
            return jsonify({'success': False, 'error': 'No files provided'}), 400
        
        files = request.files.getlist('files')
        if not files or len(files) == 0:
            return jsonify({'success': False, 'error': 'No files selected'}), 400
        
        # Initialize file handler
        file_handler = FileHandler()
        
        uploaded_files = []
        errors = []
        
        for file in files:
            if file.filename == '':
                continue
            
            # Validate and save file
            file_path, error = file_handler.save_uploaded_file(file, 'image')
            
            if error:
                errors.append(f"{file.filename}: {error}")
            else:
                uploaded_files.append({
                    'filename': file.filename,
                    'path': file_path,
                    'url': file_handler.get_file_url(file_path)
                })
        
        if errors and not uploaded_files:
            return jsonify({
                'success': False, 
                'error': 'All uploads failed',
                'details': errors
            }), 400
        
        response = {
            'success': True,
            'uploaded': uploaded_files,
            'count': len(uploaded_files)
        }
        
        if errors:
            response['warnings'] = errors
        print(errors)
        return jsonify(response)
        
    except Exception as e:
        return jsonify({
            'success': False, 
            'error': f'Upload failed: {str(e)}'
        }), 500

@reporter_bp.route('/upload/videos', methods=['POST'])
def upload_videos():
    """Handle video file uploads"""
    # Check authentication
    session_valid, session_message = InputValidator.validate_user_session(session)
    if not session_valid:
        return jsonify({'success': False, 'error': session_message}), 401
    
    if request.method != 'POST':
        return jsonify({'success': False, 'error': 'Method not allowed'}), 405
    
    try:
        # Check if files are present
        if 'files' not in request.files:
            return jsonify({'success': False, 'error': 'No files provided'}), 400
        
        files = request.files.getlist('files')
        if not files or len(files) == 0:
            return jsonify({'success': False, 'error': 'No files selected'}), 400
        
        # Initialize file handler
        file_handler = FileHandler()
        
        uploaded_files = []
        errors = []
        
        for file in files:
            if file.filename == '':
                continue
            
            # Validate and save file
            file_path, error = file_handler.save_uploaded_file(file, 'video')
            
            if error:
                errors.append(f"{file.filename}: {error}")
            else:
                uploaded_files.append({
                    'filename': file.filename,
                    'path': file_path,
                    'url': file_handler.get_file_url(file_path)
                })
        
        if errors and not uploaded_files:
            return jsonify({
                'success': False, 
                'error': 'All uploads failed',
                'details': errors
            }), 400
        
        response = {
            'success': True,
            'uploaded': uploaded_files,
            'count': len(uploaded_files)
        }
        
        if errors:
            response['warnings'] = errors
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({
            'success': False, 
            'error': f'Upload failed: {str(e)}'
        }), 500

@reporter_bp.route('/upload/status')
def upload_status():
    """Get upload status and file limits"""
    return jsonify({
        'max_files': 10,
        'max_image_size': '10MB',
        'max_video_size': '100MB',
        'allowed_image_types': ['jpg', 'jpeg', 'png', 'gif', 'webp'],
        'allowed_video_types': ['mp4', 'mov', 'avi', 'mkv', 'webm']
    })
