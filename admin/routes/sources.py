from flask import render_template, jsonify, request, redirect, url_for
from .. import admin_bp
from ..utils.auth import admin_required
from ..models.queries import get_sources_data

@admin_bp.route('/sources')
#@admin_required
def admin_sources():
    """
    News sources management page
    """
    try:
        # Get sources data
        sources_data = get_sources_data()
        
        return render_template('admin/sources.html',
                             sources_data=sources_data)
        
    except Exception as e:
        print(f"Error loading sources page: {e}")
        return render_template('admin/sources.html',
                             sources_data=[],
                             error="Failed to load sources data")

@admin_bp.route('/sources/data')
#@admin_required
def admin_sources_data():
    """
    API endpoint for sources data
    """
    try:
        sources_data = get_sources_data()
        
        return jsonify({
            "sources": sources_data,
            "count": len(sources_data)
        })
        
    except Exception as e:
        print(f"Error fetching sources data: {e}")
        return jsonify({
            "sources": [],
            "count": 0,
            "error": "Failed to fetch sources data"
        }), 500

@admin_bp.route('/analytics')
#@admin_required
def admin_analytics():
    """
    Advanced analytics dashboard
    """
    try:
        # This will be a comprehensive analytics page
        # For now, redirect to news visualization
        return redirect(url_for('admin.admin_news_visualization'))
        
    except Exception as e:
        print(f"Error loading analytics page: {e}")
        return redirect(url_for('admin.admin_dashboard'))

@admin_bp.route('/settings')
#@admin_required
def admin_settings():
    """
    Admin settings page
    """
    try:
        return render_template('admin/settings.html')
        
    except Exception as e:
        print(f"Error loading settings page: {e}")
        return render_template('admin/settings.html',
                             error="Failed to load settings")
