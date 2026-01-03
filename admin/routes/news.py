from flask import render_template, jsonify, request, redirect, url_for
from .. import admin_bp
from ..utils.auth import admin_required
from ..models.queries import (
    get_news_paginated,
    get_news_sample_for_visualization,
    get_categories_list
)
from ..utils.metrics import (
    get_category_distribution,
    get_sentiment_distribution,
    get_fake_real_ratio,
    get_credibility_distribution,
    get_news_per_source
)

@admin_bp.route('/news')
#@admin_required
def admin_news():
    """
    News management page with table view
    """
    try:
        # Get query parameters
        page = int(request.args.get('page', 1))
        category = request.args.get('category', 'all')
        search = request.args.get('search', '')
        
        # Get paginated news data
        news_data = get_news_paginated(
            page=page,
            limit=20,
            category=category,
            search=search
        )
        
        # Get categories list for filter dropdown
        categories = get_categories_list()
        
        return render_template('admin/news.html',
                             news_data=news_data,
                             categories=categories,
                             current_category=category,
                             current_search=search)
        
    except Exception as e:
        print(f"Error loading news page: {e}")
        return render_template('admin/news.html',
                             news_data={"articles": [], "total_count": 0, "current_page": 1},
                             categories=[],
                             current_category='all',
                             current_search='',
                             error="Failed to load news data")

@admin_bp.route('/news/visualization')
@admin_bp.route('/news/viz')
#@admin_required
def admin_news_visualization():
    """
    News analytics and visualization page
    """
    try:
        # Get chart data
        chart_data = {
            "category_distribution": get_category_distribution(),
            "sentiment_distribution": get_sentiment_distribution(),
            "fake_vs_real_ratio": get_fake_real_ratio(),
            "credibility_distribution": get_credibility_distribution(),
            "news_per_source": get_news_per_source()
        }
        
        # Get sample data for additional analysis
        sample_data = get_news_sample_for_visualization()
        
        return render_template('admin/news_viz.html',
                             chart_data=chart_data,
                             sample_count=len(sample_data))
        
    except Exception as e:
        print(f"Error loading news visualization: {e}")
        return render_template('admin/news_viz.html',
                             chart_data={},
                             sample_count=0,
                             error="Failed to load visualization data")

@admin_bp.route('/news/data')
#@admin_required
def admin_news_data():
    """
    API endpoint for news data with pagination
    """
    try:
        # Get query parameters
        page = int(request.args.get('page', 1))
        limit = min(int(request.args.get('limit', 50)), 100)  # Max 100 per request
        category = request.args.get('category', 'all')
        search = request.args.get('search', '')
        
        # Get news data
        news_data = get_news_paginated(
            page=page,
            limit=limit,
            category=category,
            search=search
        )
        
        return jsonify(news_data)
        
    except Exception as e:
        print(f"Error fetching news data: {e}")
        return jsonify({
            "articles": [],
            "total_count": 0,
            "total_pages": 0,
            "current_page": 1,
            "has_next": False,
            "has_prev": False,
            "error": "Failed to fetch news data"
        }), 500

@admin_bp.route('/news/charts/data')
#@admin_required
def admin_news_charts_data():
    """
    API endpoint for chart data
    """
    try:
        chart_data = {
            "category_distribution": get_category_distribution(),
            "sentiment_distribution": get_sentiment_distribution(),
            "fake_vs_real_ratio": get_fake_real_ratio(),
            "credibility_distribution": get_credibility_distribution(),
            "news_per_source": get_news_per_source()
        }
        
        return jsonify(chart_data)
        
    except Exception as e:
        print(f"Error fetching chart data: {e}")
        return jsonify({
            "category_distribution": [],
            "sentiment_distribution": [],
            "fake_vs_real_ratio": [],
            "credibility_distribution": [],
            "news_per_source": [],
            "error": "Failed to fetch chart data"
        }), 500

@admin_bp.route('/news/sample')
#@admin_required
def admin_news_sample():
    """
    API endpoint to get sample news data for analysis
    """
    try:
        sample_data = get_news_sample_for_visualization()
        
        return jsonify({
            "articles": sample_data,
            "count": len(sample_data)
        })
        
    except Exception as e:
        print(f"Error fetching news sample: {e}")
        return jsonify({
            "articles": [],
            "count": 0,
            "error": "Failed to fetch news sample"
        }), 500

@admin_bp.route('/news/<news_id>')
# @admin_required
def admin_news_details(news_id):
    """
    Render individual news article details page (or modal content)
    """
    try:
        from ..models.queries import get_news_by_id
        
        news_article = get_news_by_id(news_id)
        
        if not news_article:
            return render_template(
                "admin/404.html",
                message="News article not found"
            ), 404
        print(news_article)
        # Render template with article data
        return render_template(
            "admin/news_details.html",
            article=news_article
        )

    except Exception as e:
        print(f"Error fetching news details: {e}")
        return render_template(
            "admin/error.html",
            message="Failed to fetch news details"
        ), 500