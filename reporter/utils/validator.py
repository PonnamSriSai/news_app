import re
from datetime import datetime

class InputValidator:
    """Validates user inputs for the reporter dashboard"""
    
    @staticmethod
    def validate_full_text(text):
        """Validate the full_text field"""
        if not text or not text.strip():
            return False, "Full text is required"
        
        # Check minimum length
        if len(text.strip()) < 10:
            return False, "Full text must be at least 10 characters long"
        
        # Check maximum length
        if len(text) > 10000:
            return False, "Full text must not exceed 10,000 characters"
        
        # Check for potentially harmful content
        # Remove HTML tags and check for basic script patterns
        clean_text = re.sub(r'<[^>]+>', '', text)
        if re.search(r'<script|javascript:|on\w+\s*=', clean_text, re.IGNORECASE):
            return False, "Invalid content detected"
        
        return True, "Valid"
    
    @staticmethod
    def validate_location(location_data):
        """Validate location fields"""
        errors = []
        
        # Check if location data is provided
        if not location_data:
            return False, ["Location data is required"]
        
        # Validate district
        district = location_data.get('district', '').strip()
        if not district:
            errors.append("District is required")
        elif len(district) > 100:
            errors.append("District name too long")
        
        # Validate state
        state = location_data.get('state', '').strip()
        if not state:
            errors.append("State is required")
        elif len(state) > 100:
            errors.append("State name too long")
        
        # Validate country
        country = location_data.get('country', '').strip()
        if not country:
            errors.append("Country is required")
        elif len(country) > 100:
            errors.append("Country name too long")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def validate_source(source):
        """Validate the source field"""
        if not source or not source.strip():
            return False, "Source is required"
        
        source = source.strip()
        
        # Check length
        if len(source) > 200:
            return False, "Source must not exceed 200 characters"
        
        # Basic validation for source format
        if not re.match(r'^[a-zA-Z0-9\s\-\.\,\(\)]+$', source):
            return False, "Source contains invalid characters"
        
        return True, "Valid"
    
    @staticmethod
    def sanitize_text(text):
        """Sanitize text input"""
        if not text:
            return ""
        
        # Remove HTML tags
        clean_text = re.sub(r'<[^>]+>', '', text)
        
        # Remove potentially harmful characters
        clean_text = re.sub(r'[<>"\']', '', clean_text)
        
        # Remove extra whitespace
        clean_text = ' '.join(clean_text.split())
        
        return clean_text.strip()
    
    @staticmethod
    def validate_user_session(session):
        """Validate if user is logged in and has reporter role"""
        if not session.get('user_id'):
            return False, "User not logged in"
        
        if session.get('user_role') not in ['news_reporter', 'admin']:
            return False, "Insufficient permissions"
        
        return True, "Valid"
