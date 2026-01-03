#!/usr/bin/env python3
"""
Simple script to set up MongoDB search indexes for the news app
Run this to optimize search performance
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from setup_search_indexes import setup_search_indexes
    print("🚀 Setting up MongoDB search indexes...")
    success = setup_search_indexes()
    
    if success:
        print("\n✅ MongoDB search indexes setup completed!")
        print("\n🔧 Your search feature is now optimized for better performance.")
        print("\n📋 What was created:")
        print("   • Text search index on title, description, full_text, content, category")
        print("   • Performance indexes for categories, dates, credibility, etc.")
        print("   • Weighted search for better relevance (titles weighted highest)")
        
        print("\n🎯 Search improvements:")
        print("   • Faster text search with MongoDB full-text indexing")
        print("   • Relevance scoring for better search results")
        print("   • Optimized queries for category and date filtering")
        
        print("\n💡 Next steps:")
        print("   1. Test the search functionality in your app")
        print("   2. Run: python app.py to start the Flask server")
        print("   3. Visit: http://localhost:5000/user/dashboard/search?q=your_search_term")
        
    else:
        print("\n❌ Failed to set up indexes. Please check the error messages above.")
        
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure setup_search_indexes.py is in the same directory")
except Exception as e:
    print(f"❌ Unexpected error: {e}")

print("\n" + "="*60)
print("PSLVNews Search Index Setup")
print("="*60)
