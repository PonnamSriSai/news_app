from flask import render_template, session, redirect, url_for, flash
from .. import reporter_bp
from ..utils.validator import InputValidator

@reporter_bp.route('/dashboard')
def reporter_dashboard():
    """Main reporter dashboard"""
    # Check if user is logged in
    session_valid, session_message = InputValidator.validate_user_session(session)
    if not session_valid:
        flash('Please log in to access the reporter dashboard', 'error')
        return redirect(url_for('login'))
    
    # Check if user has news_reporter or admin role
    if session.get('user_role') not in ['news_reporter', 'admin']:
        flash('You do not have permission to access the reporter dashboard', 'error')
        return redirect(url_for('user_dashboard'))
    
    # Get recent submissions count for dashboard
    try:
        client = MongoClient(
            MONGO_URI
        )
        db = client.newsai_db
        news_master = db.news_master
        
        reporter_id = session.get('user_id')
        recent_submissions = list(
            news_master
            .find({"reporter_id": reporter_id})
            .sort("created_at", -1)
            .limit(5)
        )
        
        # Convert ObjectId to string for template usage
        for submission in recent_submissions:
            submission["_id"] = str(submission["_id"])
        
        client.close()
        
        return render_template('reporter/reporter_dashboard_new.html', recent_submissions=recent_submissions)
        
    except Exception as e:
        print(f"Error fetching recent submissions: {e}")
        return render_template('reporter/reporter_dashboard_new.html', recent_submissions=[])

# Submissions are handled by the submission.py route

@reporter_bp.route('/')
def reporter_index():
    """Redirect to dashboard"""
    return redirect(url_for('reporter.reporter_dashboard'))

@reporter_bp.route('/health')
def reporter_health():
    """Health check for reporter module"""
    return {
        'status': 'healthy',
        'module': 'reporter_dashboard',
        'timestamp': '2024-01-01T00:00:00Z'
    }
