import os
import sys
import json
from datetime import datetime
from flask import request, jsonify, session, flash, redirect, url_for, render_template
from pymongo import MongoClient
from .. import reporter_bp
from ..utils.validator import InputValidator
from ..utils.file_handler import FileHandler

# Add the utils directory to the path to import reporter_ingest
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'utils'))
from reporter_ingest import run_agent, get_sentiment, remove_emojis, now_utc, is_famous

@reporter_bp.route('/submit', methods=['POST'])
def submit_news():
    """Submit news with media files"""
    # Check authentication
    session_valid, session_message = InputValidator.validate_user_session(session)
    if not session_valid:
        return jsonify({'success': False, 'error': session_message}), 401
    
    if request.method != 'POST':
        return jsonify({'success': False, 'error': 'Method not allowed'}), 405
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        # Extract data
        full_text = data.get('full_text', '')
        source = data.get('source', '')
        location_data = data.get('location', {})
        image_paths = data.get('image_paths', [])
        video_paths = data.get('video_paths', [])
        
        # Validate full_text
        text_valid, text_message = InputValidator.validate_full_text(full_text)
        if not text_valid:
            return jsonify({'success': False, 'error': text_message}), 400
        
        # Validate source
        source_valid, source_message = InputValidator.validate_source(source)
        if not source_valid:
            return jsonify({'success': False, 'error': source_message}), 400
        
        # Validate location
        location_valid, location_errors = InputValidator.validate_location(location_data)
        if not location_valid:
            return jsonify({'success': False, 'error': 'Location validation failed', 'details': location_errors}), 400
        
        # Sanitize inputs
        full_text = InputValidator.sanitize_text(full_text)
        source = InputValidator.sanitize_text(source)
        
        # Extract location fields
        district = location_data.get('district', '').strip()
        state = location_data.get('state', '').strip()
        country = location_data.get('country', '').strip()
        
        # Process media files (convert full paths to relative paths for database)
        associate_media = {
            "images": [],
            "videos": []
        }
        
        # Process images
        for img_path in image_paths:
            if img_path and img_path.startswith('static/images/'):
                associate_media["images"].append(img_path)
        
        # Process videos
        for vid_path in video_paths:
            if vid_path and vid_path.startswith('static/videos/'):
                associate_media["videos"].append(vid_path)
        
        # Use existing reporter_ingest logic
        try:
            # Get sentiment
            sentiment_data = get_sentiment(full_text)
            
            # Get AI analysis
            agent_data, evidence_sources = run_agent(full_text)
            
            # Determine status and credibility
            published_at = now_utc().isoformat()
            
            if is_famous(source):
                status = "verified"
                credibility = 1.0
                fake_prob = 0.0
            else:
                status = "monitoring"
                credibility = agent_data.get("credibility", 0.5)
                fake_prob = agent_data.get("fake_prob", 0.5)
            
            # Construct MongoDB document using existing schema
            doc = {
                "title": agent_data.get("headline", full_text[:50]),
                "content": agent_data.get("summary", full_text),
                "full_text": full_text,
                "source": source,
                "publishedAt": published_at,
                "date": published_at[:10],
                "week": datetime.fromisoformat(published_at).isocalendar()[1],
                "month": datetime.fromisoformat(published_at).month,
                "year": datetime.fromisoformat(published_at).year,
                "category": agent_data.get("category", "general"),
                "credibility": credibility,
                "fake_prob": fake_prob,
                "summary": agent_data.get("summary", full_text[:150]),
                "time": published_at[11:19],
                "status": status,
                "associateMedia": associate_media,
                "location": {
                    "district": district,
                    "state": state,
                    "country": country
                },
                "sentiment": sentiment_data["sentiment"],
                "reporter_id": session.get('user_id'),
                "reporter_name": session.get('user_name', 'Unknown'),
                "created_at": now_utc(),
                "evidence_sources": evidence_sources
            }
            
            # Connect to MongoDB and insert
            client = MongoClient(
                        MONGO_URI
                    )
            db = client.newsai_db
            news_master = db.news_master
            
            # Insert document
            result = news_master.insert_one(doc)
            doc["_id"] = str(result.inserted_id)
            
            # Close database connection
            client.close()
            
            return jsonify({
                'success': True,
                'message': 'News submitted successfully',
                'document_id': doc["_id"],
                'title': doc["title"],
                'status': doc["status"],
                'category': doc["category"],
                'credibility': doc["credibility"],
                'fake_prob': doc["fake_prob"],
                'doc': doc
            })
            
        except Exception as e:
            return jsonify({
                'success': False,
                'error': f'AI processing failed: {str(e)}'
            }), 500
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Submission failed: {str(e)}'
        }), 500

@reporter_bp.route('/submissions', methods=['GET'])
def get_submissions():
    """Get submissions by the current reporter"""
    # Check authentication
    session_valid, session_message = InputValidator.validate_user_session(session)
    if not session_valid:
        return jsonify({'success': False, 'error': session_message}), 401
    
    try:
        # Connect to MongoDB
        client = MongoClient(
                MONGO_URI
        )
        db = client.newsai_db
        news_master = db.news_master
        
        # Get submissions by reporter
        reporter_id = session.get('user_id')
        submissions = list(
            news_master
            .find({"reporter_id": reporter_id})
            .sort("created_at", -1)
            .limit(50)
        )
        
        # Convert ObjectId to string for template usage
        for submission in submissions:
            submission["_id"] = str(submission["_id"])
            # Remove MongoDB-specific fields
            submission.pop("_id", None)
        
        client.close()
        
        return render_template('reporter/submissions_new.html', submissions=submissions)
        
    except Exception as e:
        print(f"Error fetching submissions: {e}")
        flash('Failed to load submissions. Please try again.', 'error')
        return render_template('reporter/submissions_new.html', submissions=[])

@reporter_bp.route('/submissions/api', methods=['GET'])
def get_submissions_api():
    """API endpoint to get submissions by the current reporter"""
    # Check authentication
    session_valid, session_message = InputValidator.validate_user_session(session)
    if not session_valid:
        return jsonify({'success': False, 'error': session_message}), 401
    
    try:
        # Connect to MongoDB
        client = MongoClient(
                MONGO_URI
        )
        db = client.newsai_db
        news_master = db.news_master
        
        # Get submissions by reporter
        reporter_id = session.get('user_id')
        submissions = list(
            news_master
            .find({"reporter_id": reporter_id})
            .sort("created_at", -1)
            .limit(50)
        )
        
        # Convert ObjectId to string for JSON serialization
        for submission in submissions:
            submission["_id"] = str(submission["_id"])
            # Remove MongoDB-specific fields
            submission.pop("_id", None)
        
        client.close()
        
        return jsonify({
            'success': True,
            'submissions': submissions,
            'count': len(submissions)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to fetch submissions: {str(e)}'
        }), 500
