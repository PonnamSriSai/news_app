#!/bin/bash

# News App Startup Script
# This script sets up and runs the Flask news application

echo "🚀 Starting PSLV News Application..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Check if MongoDB is accessible
echo "🔍 Checking MongoDB connection..."
python3 -c "
from pymongo import MongoClient
try:
    client = MongoClient(MONGO_URI)
    client.admin.command('ping')
    print('✅ MongoDB connection successful')
except Exception as e:
    print(f'⚠️  MongoDB connection failed: {e}')
    print('📝 Please check your MongoDB connection string')
"

# Setup search indexes
echo "🔧 Setting up search indexes..."
python3 setup_search_indexes.py --setup

echo "🎉 Setup complete!"
echo ""
echo "🌐 Starting Flask application..."
echo "📱 Access your news app at: http://localhost:5000"
echo "👤 Admin panel at: http://localhost:5000/admin"
echo ""
echo "Press Ctrl+C to stop the application"
echo "="*60

# Run the Flask application
python app.py
