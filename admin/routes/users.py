from flask import render_template, jsonify, request, redirect, url_for
from .. import admin_bp
from ..utils.auth import admin_required
from ..models.queries import (
    get_users_with_pagination,
    get_user_metrics,
    update_user_role,
    delete_user
)

@admin_bp.route('/users')
#@admin_required
def admin_users():
    """
    User management page
    """
    try:
        # Get query parameters
        page = int(request.args.get('page', 1))
        role = request.args.get('role', 'all')
        
        # Get users data
        users_data = get_users_with_pagination(
            page=page,
            limit=20,
            role=role
        )
        
        # Get user metrics
        user_metrics = get_user_metrics()
        
        return render_template('admin/users.html',
                             users_data=users_data,
                             user_metrics=user_metrics,
                             current_role=role)
        
    except Exception as e:
        print(f"Error loading users page: {e}")
        return render_template('admin/users.html',
                             users_data={"users": [], "total_count": 0, "current_page": 1},
                             user_metrics={},
                             current_role='all',
                             error="Failed to load users data")

@admin_bp.route('/users/data')
#@admin_required
def admin_users_data():
    """
    API endpoint for users data with pagination
    """
    try:
        page = int(request.args.get('page', 1))
        limit = min(int(request.args.get('limit', 50)), 100)
        role = request.args.get('role', 'all')
        
        users_data = get_users_with_pagination(
            page=page,
            limit=limit,
            role=role
        )
        
        return jsonify(users_data)
        
    except Exception as e:
        print(f"Error fetching users data: {e}")
        return jsonify({
            "users": [],
            "total_count": 0,
            "total_pages": 0,
            "current_page": 1,
            "has_next": False,
            "has_prev": False,
            "error": "Failed to fetch users data"
        }), 500

@admin_bp.route('/users/metrics')
#@admin_required
def admin_users_metrics():
    """
    API endpoint for user metrics
    """
    try:
        user_metrics = get_user_metrics()
        return jsonify(user_metrics)
        
    except Exception as e:
        print(f"Error fetching user metrics: {e}")
        return jsonify({
            "total_users": 0,
            "active_users": 0,
            "role_distribution": [],
            "error": "Failed to fetch user metrics"
        }), 500

@admin_bp.route('/users/update-role', methods=['POST'])
#@admin_required
def admin_update_user_role():
    """
    Update user role (admin function)
    """
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        new_role = data.get('role')
        
        if not user_id or not new_role:
            return jsonify({
                "success": False,
                "message": "User ID and role are required"
            }), 400
        
        if new_role not in ['admin', 'news_reporter', 'user']:
            return jsonify({
                "success": False,
                "message": "Invalid role specified"
            }), 400
        
        success = update_user_role(user_id, new_role)
        
        if success:
            return jsonify({
                "success": True,
                "message": "User role updated successfully"
            })
        else:
            return jsonify({
                "success": False,
                "message": "Failed to update user role"
            }), 500
            
    except Exception as e:
        print(f"Error updating user role: {e}")
        return jsonify({
            "success": False,
            "message": "An error occurred while updating user role"
        }), 500

@admin_bp.route('/users/delete', methods=['POST'])
#@admin_required
def admin_delete_user():
    """
    Delete user (admin function)
    """
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        
        if not user_id:
            return jsonify({
                "success": False,
                "message": "User ID is required"
            }), 400
        
        success = delete_user(user_id)
        
        if success:
            return jsonify({
                "success": True,
                "message": "User deleted successfully"
            })
        else:
            return jsonify({
                "success": False,
                "message": "Failed to delete user"
            }), 500
            
    except Exception as e:
        print(f"Error deleting user: {e}")
        return jsonify({
            "success": False,
            "message": "An error occurred while deleting user"
        }), 500
