#!/bin/bash

# Flask News Application - Production Deployment Script
# This script automates the deployment process for the Flask News Application

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
APP_NAME="Flask News Application"
APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="$APP_DIR/deployment.log"

# Functions
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}" | tee -a "$LOG_FILE"
}

error() {
    echo -e "${RED}[ERROR] $1${NC}" | tee -a "$LOG_FILE"
}

warning() {
    echo -e "${YELLOW}[WARNING] $1${NC}" | tee -a "$LOG_FILE"
}

info() {
    echo -e "${BLUE}[INFO] $1${NC}" | tee -a "$LOG_FILE"
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check Python version
check_python() {
    if ! command_exists python3; then
        error "Python 3 is not installed. Please install Python 3.8 or higher."
        exit 1
    fi
    
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d'.' -f1)
    PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d'.' -f2)
    
    if [ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -ge 8 ]; then
        log "Python version $PYTHON_VERSION is compatible"
    else
        error "Python 3.8+ is required. Current version: $PYTHON_VERSION"
        exit 1
    fi
}

# Setup virtual environment
setup_virtualenv() {
    if [ ! -d "venv" ]; then
        log "Creating virtual environment..."
        python3 -m venv venv
        log "Virtual environment created successfully"
    fi
    
    log "Activating virtual environment..."
    source venv/bin/activate
    log "Virtual environment activated"
}

# Install dependencies
install_dependencies() {
    log "Installing Python dependencies..."
    pip install --upgrade pip
    pip install -r requirements.txt
    log "Dependencies installed successfully"
}

# Setup environment file
setup_env() {
    if [ ! -f ".env" ]; then
        if [ -f ".env.example" ]; then
            cp .env.example .env
            warning "Please edit .env file with your actual configuration values"
            info "Required variables: SECRET_KEY, MONGO_URI, PINECONE_API_KEY"
            read -p "Press enter when you've configured .env file..."
        else
            error ".env.example file not found"
            exit 1
        fi
    else
        log ".env file already exists"
    fi
}

# Check environment variables
check_env_vars() {
    source .env
    
    # Check required variables
    if [ -z "$SECRET_KEY" ] || [ "$SECRET_KEY" = "your-super-secret-key-here-generate-with-secrets-token-hex-32" ]; then
        error "SECRET_KEY is not properly configured in .env file"
        exit 1
    fi
    
    if [ -z "$MONGO_URI" ] || [ "$MONGO_URI" = "mongodb+srv://your-username:your-password@your-cluster.mongodb.net/?retryWrites=true&w=majority" ]; then
        error "MONGO_URI is not properly configured in .env file"
        exit 1
    fi
    
    if [ -z "$PINECONE_API_KEY" ] || [ "$PINECONE_API_KEY" = "your-pinecone-api-key-here" ]; then
        error "PINECONE_API_KEY is not properly configured in .env file"
        exit 1
    fi
    
    log "Environment variables validated successfully"
}

# Setup database indexes
setup_database() {
    log "Setting up database indexes..."
    python3 setup_search_indexes.py --setup
    log "Database setup completed"
}

# Create necessary directories
create_directories() {
    log "Creating necessary directories..."
    mkdir -p logs uploads static/collected
    chmod 755 logs uploads static/collected
    log "Directories created successfully"
}

# Run health checks
health_check() {
    log "Running health checks..."
    
    # Test database connection
    python3 -c "
from pymongo import MongoClient
import os
try:
    client = MongoClient(os.getenv('MONGO_URI'))
    client.admin.command('ping')
    print('✅ MongoDB connection successful')
except Exception as e:
    print(f'❌ MongoDB connection failed: {e}')
    exit(1)
"
    
    # Test Flask app import
    python3 -c "
try:
    from app import app
    print('✅ Flask application imports successfully')
except Exception as e:
    print(f'❌ Flask application import failed: {e}')
    exit(1)
"
    
    log "Health checks passed successfully"
}

# Run tests
run_tests() {
    if [ -f "tests/test_app.py" ] || find . -name "*test*.py" -type f | grep -q .; then
        log "Running tests..."
        python3 -m pytest tests/ -v || warning "Some tests failed"
    else
        info "No tests found, skipping test execution"
    fi
}

# Start application
start_application() {
    local mode=${1:-development}
    
    case $mode in
        "development")
            log "Starting application in development mode..."
            python3 app.py
            ;;
        "production")
            log "Starting application in production mode..."
            if command_exists gunicorn; then
                gunicorn --bind 0.0.0.0:5000 --workers 4 --timeout 120 app:app
            else
                error "Gunicorn not found. Install with: pip install gunicorn"
                exit 1
            fi
            ;;
        "docker")
            log "Starting application with Docker..."
            if command_exists docker-compose; then
                docker-compose up --build
            else
                error "Docker Compose not found"
                exit 1
            fi
            ;;
        *)
            error "Unknown start mode: $mode"
            exit 1
            ;;
    esac
}

# Display help
show_help() {
    echo "Flask News Application Deployment Script"
    echo ""
    echo "Usage: $0 [COMMAND] [OPTIONS]"
    echo ""
    echo "Commands:"
    echo "  setup       Full setup (install dependencies, setup environment)"
    echo "  dev         Start in development mode"
    echo "  prod        Start in production mode"
    echo "  docker      Start with Docker"
    echo "  test        Run tests"
    echo "  health      Run health checks"
    echo "  clean       Clean up temporary files"
    echo "  help        Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 setup    # Full setup"
    echo "  $0 dev      # Start development server"
    echo "  $0 prod     # Start production server"
    echo "  $0 docker   # Start with Docker Compose"
    echo ""
}

# Clean up temporary files
cleanup() {
    log "Cleaning up temporary files..."
    find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
    find . -name "*.pyc" -delete 2>/dev/null || true
    find . -name ".pytest_cache" -type d -exec rm -rf {} + 2>/dev/null || true
    find . -name "*.egg-info" -type d -exec rm -rf {} + 2>/dev/null || true
    log "Cleanup completed"
}

# Main execution
main() {
    log "Starting deployment for $APP_NAME"
    
    case ${1:-setup} in
        "setup")
            check_python
            setup_virtualenv
            install_dependencies
            setup_env
            check_env_vars
            create_directories
            setup_database
            health_check
            run_tests
            log "Setup completed successfully!"
            info "Run '$0 dev' to start the development server"
            ;;
        "dev")
            check_python
            setup_virtualenv
            check_env_vars
            create_directories
            start_application development
            ;;
        "prod")
            check_python
            setup_virtualenv
            check_env_vars
            create_directories
            start_application production
            ;;
        "docker")
            check_env_vars
            create_directories
            start_application docker
            ;;
        "test")
            setup_virtualenv
            run_tests
            ;;
        "health")
            check_env_vars
            health_check
            ;;
        "clean")
            cleanup
            ;;
        "help"|"-h"|"--help")
            show_help
            ;;
        *)
            error "Unknown command: $1"
            show_help
            exit 1
            ;;
    esac
}

# Trap errors
trap 'error "Script failed at line $LINENO. Exit code: $?"' ERR

# Run main function
main "$@"
