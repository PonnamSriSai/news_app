from datetime import datetime, date, timedelta
from pymongo import MongoClient
from collections import Counter
import statistics

# MongoDB connection
client = MongoClient(
    MONGO_URI
)
db = client.newsai_db  # Use newsai_db for news data
news_master = db.news_master
users_collection = db.users

def get_today_metrics():
    """
    Get today's news metrics
    """
    today = datetime.now().date().strftime("%Y-%m-%d")
    
    try:
        # Today's metrics aggregation
        pipeline = [
            {
                "$match": {
                    "date": today  # Match today's articles
                }
            },
            {
                "$group": {
                    "_id": None,
                    "total_articles": {"$sum": 1},
                    "fake_news_detected": {
                        "$sum": {"$cond": [{"$gt": ["$fake_prob", 50]}, 1, 0]}
                    },
                    "avg_credibility": {"$avg": "$credibility"},
                    "avg_sentiment": {"$avg": "$sentiment_score"}
                }
            }
        ]
        
        result = list(news_master.aggregate(pipeline))
        
        if result:
            metrics = result[0]
        else:
            metrics = {
                "total_articles": 0,
                "fake_news_detected": 0,
                "avg_credibility": 0,
                "avg_sentiment": 0
            }
        
        # Get most common sentiment for today
        sentiment_pipeline = [
            {"$match": {"date": today}},
            {"$group": {"_id": "$sentiment_score", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": 1}
        ]
        
        sentiment_result = list(news_master.aggregate(sentiment_pipeline))
        most_common_sentiment = sentiment_result[0]["_id"] if sentiment_result else 0
        
        return {
            "total_articles": metrics["total_articles"],
            "fake_news_detected": metrics["fake_news_detected"],
            "avg_credibility": round(metrics["avg_credibility"] * 100, 1) if metrics["avg_credibility"] else 0,
            "avg_sentiment": round(metrics["avg_sentiment"], 3) if metrics["avg_sentiment"] else 0,
            "most_common_sentiment": round(most_common_sentiment, 3)
        }
        
    except Exception as e:
        print(f"Error getting today metrics: {e}")
        return {
            "total_articles": 0,
            "fake_news_detected": 0,
            "avg_credibility": 0,
            "avg_sentiment": 0,
            "most_common_sentiment": 0
        }

def get_overall_metrics():
    """
    Get overall news metrics from entire database
    """
    try:
        # Overall metrics aggregation
        pipeline = [
            {
                "$group": {
                    "_id": None,
                    "total_articles": {"$sum": 1},
                    "fake_news_detected": {
                        "$sum": {"$cond": [{"$gt": ["$fake_prob", 50]}, 1, 0]}
                    },
                    "avg_credibility": {"$avg": "$credibility"},
                    "avg_sentiment": {"$avg": "$sentiment_score"}
                }
            }
        ]
        
        result = list(news_master.aggregate(pipeline))
        
        if result:
            metrics = result[0]
        else:
            metrics = {
                "total_articles": 0,
                "fake_news_detected": 0,
                "avg_credibility": 0,
                "avg_sentiment": 0
            }
        
        # Get most common sentiment overall
        sentiment_pipeline = [
            {"$group": {"_id": "$sentiment_score", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": 1}
        ]
        
        sentiment_result = list(news_master.aggregate(sentiment_pipeline))
        most_common_sentiment = sentiment_result[0]["_id"] if sentiment_result else 0
        
        return {
            "total_articles": metrics["total_articles"],
            "fake_news_detected": metrics["fake_news_detected"],
            "avg_credibility": round(metrics["avg_credibility"] * 100, 1) if metrics["avg_credibility"] else 0,
            "avg_sentiment": round(metrics["avg_sentiment"], 3) if metrics["avg_sentiment"] else 0,
            "most_common_sentiment": round(most_common_sentiment, 3)
        }
        
    except Exception as e:
        print(f"Error getting overall metrics: {e}")
        return {
            "total_articles": 0,
            "fake_news_detected": 0,
            "avg_credibility": 0,
            "avg_sentiment": 0,
            "most_common_sentiment": 0
        }

def get_category_distribution():
    """
    Get category distribution for news articles
    """
    try:
        pipeline = [
            {"$group": {"_id": "$category", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}
        ]
        
        result = list(news_master.aggregate(pipeline))
        return [{"category": item["_id"], "count": item["count"]} for item in result]
        
    except Exception as e:
        print(f"Error getting category distribution: {e}")
        return []

def get_sentiment_distribution():
    """
    Get sentiment score distribution
    """
    try:
        # Get all sentiment scores and categorize them
        pipeline = [
            {"$project": {
                "sentiment_category": {
                    "$switch": {
                        "branches": [
                            {"case": {"$lt": ["$sentiment_score", -0.5]}, "then": "Very Negative"},
                            {"case": {"$lt": ["$sentiment_score", -0.1]}, "then": "Negative"},
                            {"case": {"$lt": ["$sentiment_score", 0.1]}, "then": "Neutral"},
                            {"case": {"$lt": ["$sentiment_score", 0.5]}, "then": "Positive"}
                        ],
                        "default": "Very Positive"
                    }
                }
            }},
            {"$group": {"_id": "$sentiment_category", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}
        ]
        
        result = list(news_master.aggregate(pipeline))
        return [{"sentiment": item["_id"], "count": item["count"]} for item in result]
        
    except Exception as e:
        print(f"Error getting sentiment distribution: {e}")
        return []

def get_fake_real_ratio():
    """
    Get fake vs real news ratio
    """
    try:
        pipeline = [
            {
                "$addFields": {
                    "news_type": {
                        "$cond": [{"$gt": ["$fake_prob", 50]}, "Fake News", "Real News"]
                    }
                }
            },
            {"$group": {"_id": "$news_type", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}
        ]
        
        result = list(news_master.aggregate(pipeline))
        return [{"type": item["_id"], "count": item["count"]} for item in result]
        
    except Exception as e:
        print(f"Error getting fake real ratio: {e}")
        return []

def get_credibility_distribution():
    """
    Get credibility score distribution
    """
    try:
        pipeline = [
            {
                "$addFields": {
                    "credibility_range": {
                        "$switch": {
                            "branches": [
                                {"case": {"$lt": ["$credibility", 0.2]}, "then": "0.0-0.2"},
                                {"case": {"$lt": ["$credibility", 0.4]}, "then": "0.2-0.4"},
                                {"case": {"$lt": ["$credibility", 0.6]}, "then": "0.4-0.6"},
                                {"case": {"$lt": ["$credibility", 0.8]}, "then": "0.6-0.8"}
                            ],
                            "default": "0.8-1.0"
                        }
                    }
                }
            },
            {"$group": {"_id": "$credibility_range", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}
        ]
        
        result = list(news_master.aggregate(pipeline))
        return [{"range": item["_id"], "count": item["count"]} for item in result]
        
    except Exception as e:
        print(f"Error getting credibility distribution: {e}")
        return []

def get_news_per_source():
    """
    Get news count per source
    """
    try:
        pipeline = [
            {"$group": {"_id": "$source", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": 10}  # Top 10 sources
        ]
        
        result = list(news_master.aggregate(pipeline))
        return [{"source": item["_id"], "count": item["count"]} for item in result]
        
    except Exception as e:
        print(f"Error getting news per source: {e}")
        return []

def get_preview_data():
    """
    Get preview counts for dashboard cards
    """
    try:
        news_count = news_master.count_documents({})
        users_count = users_collection.count_documents({})
        
        # Get sources count
        sources_pipeline = [
            {"$group": {"_id": "$source"}},
            {"$count": "total_sources"}
        ]
        
        sources_result = list(news_master.aggregate(sources_pipeline))
        sources_count = sources_result[0]["total_sources"] if sources_result else 0
        
        return {
            "news_count": news_count,
            "users_count": users_count,
            "sources_count": sources_count
        }
        
    except Exception as e:
        print(f"Error getting preview data: {e}")
        return {
            "news_count": 0,
            "users_count": 0,
            "sources_count": 0
        }
