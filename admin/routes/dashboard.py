from flask import render_template, jsonify, request, redirect, url_for
from datetime import datetime

from .. import admin_bp
from ..utils.auth import admin_required
from ..utils.metrics import (
    get_today_metrics, 
    get_overall_metrics, 
    get_preview_data
)
from ..models.queries import (
    get_news_paginated, 
    get_user_metrics, 
    get_sources_data
)


@admin_bp.route('/dashboard')
#@admin_required
def admin_dashboard():
    """
    Main admin dashboard with today's and overall metrics
    """
    try:
        # Get today's metrics
        today_metrics = get_today_metrics()
        
        # Get overall metrics
        overall_metrics = get_overall_metrics()
        
        # Get preview data for quick access cards
        preview_data = get_preview_data()
        
        # Get recent news for quick preview
        recent_news = get_news_paginated(page=1, limit=5)
        
        return render_template('admin/dashboard.html',
                             today_metrics=today_metrics,
                            today = datetime.utcnow(),
                             overall_metrics=overall_metrics,
                             preview_data=preview_data,
                             recent_news=recent_news["articles"])
        
    except Exception as e:
        print(f"Error loading admin dashboard: {e}")
        return render_template('admin/dashboard.html',
                             today_metrics={},
                             overall_metrics={},
                             preview_data={},
                             recent_news=[],
                             error="Failed to load dashboard data")

@admin_bp.route('/')
def admin_index():
    """
    Redirect admin root to dashboard
    """
    return redirect(url_for('admin.admin_dashboard'))

@admin_bp.route('/health')
def admin_health():
    """
    Health check endpoint for admin module
    """
    return jsonify({
        "status": "healthy",
        "module": "admin",
        "timestamp": "2024-01-01T00:00:00Z"
    })
