from functools import wraps
from flask import jsonify, redirect, url_for, session
from bson import ObjectId
from pymongo import MongoClient

# MongoDB connection
client = MongoClient(
    MONGO_URI
)
db = client.pslvnews
users = db.users

def admin_required(f):
    """
    Decorator to ensure only admin users can access admin routes
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if user is logged in
        if 'user_id' not in session:
            return redirect(url_for('login'))
        
        # Get current user from database
        try:
            user = users.find_one({"_id": ObjectId(session['user_id'])})
            if not user:
                session.clear()
                return redirect(url_for('login'))
            
            # Check if user has admin role
            if user.get('role') != 'admin':
                return jsonify({
                    "error": "Access denied. Admin privileges required.",
                    "redirect": url_for('user_dashboard')
                }), 403

            return f(*args, **kwargs)
            
        except Exception as e:
            print(f"Error in admin_required: {e}")
            session.clear()
            return redirect(url_for('login'))
    
    return decorated_function

def get_admin_user():
    """
    Helper function to get current admin user
    """
    if 'user_id' not in session:
        return None
    
    try:
        user = users.find_one({"_id": ObjectId(session['user_id'])})
        return user if user and user.get('role') == 'admin' else None
    except:
        return None

def validate_admin_session():
    """
    Validate if current session has admin access
    """
    user = get_admin_user()
    if not user:
        return False, "Not authenticated as admin"
    
    return True, user
