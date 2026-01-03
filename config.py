"""
Production Configuration for Flask News Application
This file contains production-specific settings and configurations.
"""

import os
from datetime import timedelta


class ProductionConfig:
    """Production configuration settings."""
    
    # Application Settings
    SECRET_KEY = os.getenv('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY environment variable is required in production")
    
    # Flask Settings
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False
    
    # Server Settings
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 5000))
    SSL_DISABLE = os.getenv('SSL_DISABLE', 'True').lower() == 'false'
    
    # Database Settings
    MONGO_URI = os.getenv('MONGO_URI')
    if not MONGO_URI:
        raise ValueError("MONGO_URI environment variable is required in production")
    
    DB_NAME = os.getenv('DB_NAME', 'pslvnews')
    NEWS_DB_NAME = os.getenv('NEWS_DB_NAME', 'newsai_db')
    
    # Security Settings
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    
    # CSRF Protection
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = 3600
    
    # File Upload Settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
    
    # AI Services
    PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
    ASSISTANT_NAME = os.getenv('ASSISTANT_NAME', 'news')
    
    # Logging Configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE_PATH', 'logs/production.log')
    
    # Ensure logs directory exists
    @staticmethod
    def ensure_log_directory():
        """Ensure the log directory exists."""
        log_dir = os.path.dirname(ProductionConfig.LOG_FILE)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
    
    # Rate Limiting
    RATELIMIT_STORAGE_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    RATELIMIT_DEFAULT = '100 per hour'
    RATELIMIT_HEADERS_ENABLED = True
    
    # Cache Settings
    CACHE_TYPE = 'redis'
    CACHE_REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    CACHE_DEFAULT_TIMEOUT = 300
    
    # Email Settings (for notifications)
    MAIL_SERVER = os.getenv('SMTP_SERVER')
    MAIL_PORT = int(os.getenv('SMTP_PORT', 587))
    MAIL_USE_TLS = os.getenv('SMTP_USE_TLS', 'true').lower() == 'true'
    MAIL_USERNAME = os.getenv('SMTP_USERNAME')
    MAIL_PASSWORD = os.getenv('SMTP_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('FROM_EMAIL')
    
    # Monitoring & Analytics
    SENTRY_DSN = os.getenv('SENTRY_DSN')
    
    # Trusted Hosts (for security)
    TRUSTED_HOSTS = os.getenv('TRUSTED_HOSTS', 'localhost').split(',')
    
    # MongoDB Connection Pool Settings
    MONGO_CONNECT = True
    MONGO_SERVER_SELECTION_TIMEOUT_MS = 5000
    MONGO_CONNECT_TIMEOUT_MS = 10000
    MONGO_MAX_POOL_SIZE = 20
    MONGO_MIN_POOL_SIZE = 5
    
    # Content Security Policy
    SECURITY_HEADERS = {
        'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
        'X-Content-Type-Options': 'nosniff',
        'X-Frame-Options': 'DENY',
        'X-XSS-Protection': '1; mode=block',
        'Referrer-Policy': 'strict-origin-when-cross-origin'
    }
    
    # API Rate Limiting
    API_RATE_LIMIT = os.getenv('API_RATE_LIMIT', '1000')
    
    # Background Tasks
    CELERY_BROKER_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    CELERY_RESULT_BACKEND = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    
    @staticmethod
    def init_app(app):
        """Initialize the application with production settings."""
        # Ensure log directory exists
        ProductionConfig.ensure_log_directory()
        
        # Configure logging
        import logging
        from logging.handlers import RotatingFileHandler
        
        if not app.debug:
            # Create file handler for production logs
            file_handler = RotatingFileHandler(
                ProductionConfig.LOG_FILE, 
                maxBytes=10240000,  # 10MB
                backupCount=10
            )
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
            ))
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)
            
            app.logger.setLevel(logging.INFO)
            app.logger.info('Flask News App startup in production mode')
        
        # Configure security headers
        @app.after_request
        def add_security_headers(response):
            """Add security headers to all responses."""
            for header, value in ProductionConfig.SECURITY_HEADERS.items():
                response.headers[header] = value
            return response


class DevelopmentConfig:
    """Development configuration settings."""
    
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = False
    
    # Database Settings
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/pslvnews')
    DB_NAME = os.getenv('DB_NAME', 'pslvnews')
    NEWS_DB_NAME = os.getenv('NEWS_DB_NAME', 'newsai_db')
    
    # Development-specific settings
    SESSION_COOKIE_SECURE = False
    WTF_CSRF_ENABLED = False  # Disable CSRF in development for easier testing
    
    # Logging
    LOG_LEVEL = 'DEBUG'
    
    # AI Services (use test/dev keys in development)
    PINECONE_API_KEY = os.getenv('PINECONE_API_KEY', 'dev-pinecone-key')
    ASSISTANT_NAME = os.getenv('ASSISTANT_NAME', 'news-dev')
    
    @staticmethod
    def init_app(app):
        """Initialize the application with development settings."""
        # Development logging
        app.logger.setLevel(logging.DEBUG)


class TestingConfig:
    """Testing configuration settings."""
    
    SECRET_KEY = os.getenv('SECRET_KEY', 'test-secret-key')
    TESTING = True
    DEBUG = True
    
    # Use in-memory database or test database
    MONGO_URI = os.getenv('TEST_DATABASE_URL', 'mongodb://localhost:27017/test_news_db')
    DB_NAME = os.getenv('TEST_DB_NAME', 'test_pslvnews')
    NEWS_DB_NAME = os.getenv('TEST_NEWS_DB_NAME', 'test_newsai_db')
    
    # Disable CSRF for testing
    WTF_CSRF_ENABLED = False
    
    # Use test AI services
    PINECONE_API_KEY = os.getenv('TEST_PINECONE_API_KEY', 'test-pinecone-key')
    
    # Disable email sending during tests
    MAIL_SUPPRESS_SEND = True
    
    @staticmethod
    def init_app(app):
        """Initialize the application with testing settings."""
        # Testing logging
        app.logger.setLevel(logging.DEBUG)


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
