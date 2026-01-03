# Testing Framework for Flask News Application

import pytest
import os
import sys
from flask import Flask
from pymongo import MongoClient
import tempfile
import shutil

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from config import TestingConfig


@pytest.fixture(scope="session")
def app():
    """Create a Flask application for testing."""
    app = create_app(TestingConfig)
    app.config['TESTING'] = True
    
    with app.app_context():
        yield app


@pytest.fixture
def client(app):
    """Create a test client for the application."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Create a test CLI runner for the application."""
    return app.test_cli_runner()


@pytest.fixture(scope="session")
def database():
    """Set up a test database."""
    # Use a separate test database
    test_db_name = "test_news_app"
    mongo_uri = os.getenv('TEST_DATABASE_URL', 'mongodb://localhost:27017/')
    
    client = MongoClient(mongo_uri)
    
    # Create test database
    test_db = client[test_db_name]
    
    yield test_db
    
    # Clean up after tests
    client.drop_database(test_db_name)
    client.close()


@pytest.fixture
def sample_user_data():
    """Sample user data for testing."""
    return {
        "first_name": "Test",
        "last_name": "User",
        "email": "test@example.com",
        "age": 25,
        "location": "Test City",
        "role": "user",
        "password": "testpassword123"
    }


@pytest.fixture
def sample_news_data():
    """Sample news data for testing."""
    return {
        "title": "Test News Article",
        "description": "This is a test news article for unit testing.",
        "content": "Full content of the test news article goes here.",
        "category": "technology",
        "status": "published",
        "source": "Test Source",
        "published_at": "2024-01-01T00:00:00Z"
    }


# Helper functions for tests
def create_test_user(client, user_data):
    """Helper function to create a test user."""
    response = client.post('/register', data=user_data, follow_redirects=True)
    return response


def login_user(client, email, password):
    """Helper function to login a user."""
    return client.post('/login', data={
        'email': email,
        'password': password
    }, follow_redirects=True)


def create_test_news(client, news_data, token=None):
    """Helper function to create test news."""
    headers = {}
    if token:
        headers['Authorization'] = f'Bearer {token}'
    
    return client.post('/admin/news', 
                      data=news_data, 
                      headers=headers,
                      follow_redirects=True)


# Custom test configuration
pytest_plugins = ('celery.contrib.pytest',)


def pytest_configure(config):
    """Configure pytest."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests"
    )


# Test database setup
@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """Set up the test database before running tests."""
    # This fixture runs once for the entire test session
    test_db_name = "test_news_app"
    mongo_uri = os.getenv('TEST_DATABASE_URL', 'mongodb://localhost:27017/')
    
    client = MongoClient(mongo_uri)
    
    # Ensure test database exists
    test_db = client[test_db_name]
    
    # Create test indexes
    try:
        test_db.news_master.create_index([("title", "text"), ("content", "text")])
        test_db.users.create_index("email", unique=True)
    except Exception as e:
        print(f"Warning: Could not create test indexes: {e}")
    
    yield test_db
    
    # Cleanup after all tests
    try:
        client.drop_database(test_db_name)
    except Exception as e:
        print(f"Warning: Could not drop test database: {e}")
    finally:
        client.close()


# Environment variables for testing
@pytest.fixture(autouse=True)
def setup_test_env():
    """Set up environment variables for testing."""
    os.environ['TESTING'] = 'True'
    os.environ['SECRET_KEY'] = 'test-secret-key-for-testing'
    os.environ['MONGO_URI'] = os.getenv('TEST_DATABASE_URL', 'mongodb://localhost:27017/test_news_app')
    os.environ['DB_NAME'] = 'test_pslvnews'
    os.environ['NEWS_DB_NAME'] = 'test_newsai_db'
    os.environ['PINECONE_API_KEY'] = 'test-pinecone-key'
    
    yield
    
    # Clean up environment variables
    test_vars = ['TESTING', 'SECRET_KEY', 'MONGO_URI', 'DB_NAME', 'NEWS_DB_NAME', 'PINECONE_API_KEY']
    for var in test_vars:
        os.environ.pop(var, None)
