from datetime import datetime, timedelta
from pymongo import MongoClient, ASCENDING, DESCENDING
from bson import ObjectId
import math

# MongoDB connection
client = MongoClient(
    MON
)
db = client.newsai_db  # Use newsai_db for news data
news_master = db.news_master
users_collection = db.users

def get_news_paginated(page=1, limit=50, category=None, search=None):
    """
    Get news articles with pagination and filtering
    """
    try:
        # Build query
        query = {}
        
        if category and category != "all":
            query["category"] = category
        
        if search:
            query["$or"] = [
                {"title": {"$regex": search, "$options": "i"}},
                {"content": {"$regex": search, "$options": "i"}},
                {"source": {"$regex": search, "$options": "i"}}
            ]
        
        # Calculate skip
        skip = (page - 1) * limit
        
        # Get total count for pagination
        total_count = news_master.count_documents(query)
        total_pages = math.ceil(total_count / limit)
        
        # Get articles
        articles = list(
            news_master.find(query)
            .sort("publishedAt", -1)
            .skip(skip)
            .limit(limit)
        )
        
        # Convert ObjectId to string for JSON serialization
        for article in articles:
            article["_id"] = str(article["_id"])
        
        return {
            "articles": articles,
            "total_count": total_count,
            "total_pages": total_pages,
            "current_page": page,
            "has_next": page < total_pages,
            "has_prev": page > 1
        }
        
    except Exception as e:
        print(f"Error getting paginated news: {e}")
        return {
            "articles": [],
            "total_count": 0,
            "total_pages": 0,
            "current_page": 1,
            "has_next": False,
            "has_prev": False
        }

def get_news_sample_for_visualization():
    """
    Get a representative sample of news for visualization (max 1000 articles)
    """
    try:
        # Get recent articles with good distribution across categories
        pipeline = [
            {"$sort": {"publishedAt": -1}},
            {"$limit": 1000}  # Limit for performance
        ]
        
        articles = list(news_master.aggregate(pipeline))
        
        # Convert ObjectId to string
        for article in articles:
            article["_id"] = str(article["_id"])
        
        return articles
        
    except Exception as e:
        print(f"Error getting news sample for visualization: {e}")
        return []

def get_users_with_pagination(page=1, limit=50, role=None):
    """
    Get users with pagination and role filtering
    """
    try:
        # Build query
        query = {}
        if role and role != "all":
            query["role"] = role
        
        # Calculate skip
        skip = (page - 1) * limit
        
        # Get total count
        total_count = users_collection.count_documents(query)
        total_pages = math.ceil(total_count / limit)
        
        # Get users
        users = list(
            users_collection.find(query)
            .sort("created_at", -1)
            .skip(skip)
            .limit(limit)
        )
        
        # Convert ObjectId to string
        for user in users:
            user["_id"] = str(user["_id"])
        
        return {
            "users": users,
            "total_count": total_count,
            "total_pages": total_pages,
            "current_page": page,
            "has_next": page < total_pages,
            "has_prev": page > 1
        }
        
    except Exception as e:
        print(f"Error getting users: {e}")
        return {
            "users": [],
            "total_count": 0,
            "total_pages": 0,
            "current_page": 1,
            "has_next": False,
            "has_prev": False
        }

def get_user_metrics():
    """
    Get user-related metrics for admin dashboard
    """
    try:
        # Total users
        total_users = users_collection.count_documents({})
        
        # Role distribution
        role_pipeline = [
            {"$group": {"_id": "$role", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}
        ]
        role_distribution = list(users_collection.aggregate(role_pipeline))
        
        # Active users (created in last 30 days)
        thirty_days_ago = datetime.now() - timedelta(days=30)
        active_users = users_collection.count_documents({
            "created_at": {"$gte": thirty_days_ago}
        })
        
        return {
            "total_users": total_users,
            "active_users": active_users,
            "role_distribution": role_distribution
        }
        
    except Exception as e:
        print(f"Error getting user metrics: {e}")
        return {
            "total_users": 0,
            "active_users": 0,
            "role_distribution": []
        }

def get_sources_data():
    """
    Get sources data with metrics
    """
    try:
        pipeline = [
            {
                "$group": {
                    "_id": "$source",
                    "article_count": {"$sum": 1},
                    "avg_credibility": {"$avg": "$credibility"},
                    "fake_news_count": {
                        "$sum": {"$cond": [{"$gt": ["$fake_prob", 50]}, 1, 0]}
                    },
                    "avg_sentiment": {"$avg": "$sentiment_score"}
                }
            },
            {"$sort": {"article_count": -1}}
        ]
        
        sources = list(news_master.aggregate(pipeline))
        
        return sources
        
    except Exception as e:
        print(f"Error getting sources data: {e}")
        return []

def update_user_role(user_id, new_role):
    """
    Update user role (admin function)
    """
    try:
        result = users_collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"role": new_role}}
        )
        return result.modified_count > 0
    except Exception as e:
        print(f"Error updating user role: {e}")
        return False

def delete_user(user_id):
    """
    Delete user (admin function)
    """
    try:
        result = users_collection.delete_one({"_id": ObjectId(user_id)})
        return result.deleted_count > 0
    except Exception as e:
        print(f"Error deleting user: {e}")
        return False

def get_categories_list():
    """
    Get list of all news categories
    """
    try:
        pipeline = [
            {"$group": {"_id": "$category"}},
            {"$sort": {"_id": 1}}
        ]
        
        categories = list(news_master.aggregate(pipeline))
        return [cat["_id"] for cat in categories if cat["_id"]]
        
    except Exception as e:
        print(f"Error getting categories: {e}")
        return []

def get_news_by_id(news_id):
    """
    Get a single news article by ID
    """
    try:
        # Convert string ID to ObjectId
        article = news_master.find_one({"_id": ObjectId(news_id)})
        
        if article:
            # Convert ObjectId to string for JSON serialization
            article["_id"] = str(article["_id"])
            return article
        
        return None
        
    except Exception as e:
        print(f"Error getting news by ID: {e}")
        return None
