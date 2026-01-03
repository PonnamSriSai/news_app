#!/usr/bin/env python3
"""
MongoDB Search Index Setup Script
This script creates text indexes for optimal search performance across news articles.
Run this script to set up the search indexes for the first time.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pymongo import MongoClient, TEXT, ASCENDING, DESCENDING

def setup_search_indexes():
    """Create text indexes for optimal search performance"""
    
    # MongoDB connection
    client = MongoClient(
        MONGOURI
    )
    
    try:
        db = client.newsai_db
        collection = db.news_master
        
        print("🔍 Setting up MongoDB search indexes...")
        
        # Drop existing text indexes to avoid conflicts
        existing_indexes = collection.list_indexes()
        for index in existing_indexes:
            index_name = index.get('name', '')
            if index_name != '_id_' and 'text' in index_name:
                print(f"🗑️  Dropping existing text index: {index_name}")
                collection.drop_index(index_name)
        
        # Create compound text index for search fields
        print("📝 Creating compound text index...")
        collection.create_index([
            ('title', TEXT),
            ('description', TEXT),
            ('full_text', TEXT),
            ('content', TEXT),
            ('category', TEXT)
        ], 
        name='search_text_index',
        weights={
            'title': 10,        # Highest weight for titles
            'description': 5,   # Medium weight for descriptions
            'full_text': 3,     # Lower weight for full text
            'content': 3,       # Lower weight for content
            'category': 2       # Lowest weight for categories
        })
        
        # Create regular indexes for performance
        print("⚡ Creating regular performance indexes...")
        
        # Index for category-based queries (existing functionality)
        collection.create_index([('category', ASCENDING)], name='category_index')
        
        # Index for date sorting (existing functionality)
        collection.create_index([('created_at', DESCENDING)], name='date_index')
        
        # Index for combined category and date queries
        collection.create_index([
            ('category', ASCENDING),
            ('created_at', DESCENDING)
        ], name='category_date_index')
        
        # Index for credibility-based sorting
        collection.create_index([('credibility', DESCENDING)], name='credibility_index')
        
        # Index for sentiment analysis
        collection.create_index([('sentiment_score', DESCENDING)], name='sentiment_index')
        
        # Index for likes/rating
        collection.create_index([('likes', DESCENDING)], name='likes_index')
        
        # Verify indexes were created
        print("\n✅ Created indexes:")
        indexes = collection.list_indexes()
        for index in indexes:
            index_name = index.get('name', 'Unknown')
            if index_name != '_id_':
                print(f"   • {index_name}")
        
        print("\n🎉 Search index setup completed successfully!")
        print("\n💡 Tips for optimal performance:")
        print("   • Use text search with $text query for better relevance scoring")
        print("   • Combine text search with regular indexes for filtering")
        print("   • Monitor query performance with .explain()")
        
        # Example usage
        print("\n📋 Example usage in your Flask app:")
        print("""
# Text search with relevance scoring
results = collection.find(
    {"$text": {"$search": "politics election"}},
    {"score": {"$meta": "textScore"}}
).sort([("score", {"$meta": "textScore"})])

# Combined text search with category filter
results = collection.find({
    "$and": [
        {"$text": {"$search": "technology"}},
        {"category": "technology"}
    ]
}).sort([("score", {"$meta": "textScore"})])
        """)
        
    except Exception as e:
        print(f"❌ Error setting up indexes: {str(e)}")
        return False
    
    finally:
        client.close()
    
    return True

def check_indexes():
    """Check current indexes"""
    client = MongoClient(
        MONGO_URI
    )
    
    try:
        db = client.newsai_db
        collection = db.news_master
        
        print("🔍 Current indexes:")
        indexes = collection.list_indexes()
        for index in indexes:
            index_name = index.get('name', 'Unknown')
            index_keys = list(index.get('key', {}).keys())
            print(f"   • {index_name}: {index_keys}")
            
    except Exception as e:
        print(f"❌ Error checking indexes: {str(e)}")
    
    finally:
        client.close()

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Setup MongoDB search indexes')
    parser.add_argument('--check', action='store_true', help='Check current indexes')
    parser.add_argument('--setup', action='store_true', help='Setup search indexes')
    
    args = parser.parse_args()
    
    if args.check:
        check_indexes()
    elif args.setup:
        setup_search_indexes()
    else:
        print("MongoDB Search Index Setup")
        print("Usage: python setup_search_indexes.py --setup")
        print("       python setup_search_indexes.py --check")
        print("\nUse --setup to create indexes, --check to view current indexes")
