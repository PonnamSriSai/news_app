# 📰 Flask News Application

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.1%2B-green.svg)](https://flask.palletsprojects.com)
[![MongoDB](https://img.shields.io/badge/MongoDB-6.0%2B-brightgreen.svg)](https://mongodb.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A comprehensive Flask-based news aggregation and analysis platform with AI-powered features, role-based access control, and advanced search capabilities.

## 🚀 Features

### 📊 **News Management**
- **Multi-category news organization** (Breaking News, Politics, Sports, Technology, etc.)
- **Real-time news aggregation** from multiple sources
- **Advanced search functionality** with MongoDB text indexing
- **News credibility analysis** using AI
- **Sentiment analysis** for news articles
- **Breaking news priority system**

### 🔐 **User Management**
- **Role-based access control** (Admin, News Reporter, User)
- **Secure authentication** with Flask-Bcrypt
- **User preferences** and reading history
- **Category-based news filtering**
- **Personalized news feeds**

### 🤖 **AI-Powered Features**
- **Pinecone AI integration** for intelligent news analysis
- **Automated news credibility scoring**
- **Fake news detection** with confidence scoring
- **Content summarization**
- **Evidence source verification**
- **Chatbot integration** for news queries

### 📱 **User Interfaces**
- **Responsive web design** for all devices
- **Admin dashboard** for content management
- **Reporter portal** for news submission
- **User dashboard** with personalized feeds
- **News analysis interface**

### 🔍 **Advanced Search & Analysis**
- **Full-text search** across news articles
- **Category-based filtering**
- **Date range filtering**
- **Search result ranking**
- **Real-time search suggestions**

## 🏗️ **Project Structure**

```
news_app/
├── 📁 admin/                 # Admin blueprint
│   ├── 📁 models/           # Database models
│   ├── 📁 routes/           # Admin routes
│   └── 📁 utils/            # Admin utilities
├── 📁 reporter/             # Reporter blueprint
│   ├── 📁 routes/           # Reporter routes
│   ├── 📁 static/           # Static files
│   ├── 📁 templates/        # Reporter templates
│   └── 📁 utils/            # Reporter utilities
├── 📁 static/               # Global static files
│   ├── 📁 css/              # Stylesheets
│   ├── 📁 js/               # JavaScript files
│   └── 📁 images/           # Images
├── 📁 templates/            # Global templates
├── 📁 utils/                # Utility functions
├── app.py                   # Main application entry
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
├── .gitignore              # Git ignore patterns
├── setup_search_indexes.py # Database index setup
└── run.sh                  # Application startup script
```

## 📋 **Prerequisites**

- **Python 3.8+**
- **MongoDB** (local or cloud instance)
- **Pinecone account** (for AI features)
- **Git** (for cloning the repository)

## ⚡ **Quick Start**

### 1. **Clone the Repository**
```bash
git clone https://github.com/PonnamSriSai/news_app.git
cd news_app
```

### 2. **Set Up Virtual Environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

### 4. **Configure Environment Variables**
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your actual values
nano .env
```

### 5. **Set Up MongoDB Search Indexes**
```bash
python setup_search_indexes.py --setup
```

### 6. **Run the Application**
```bash
# Using the startup script
./run.sh

# Or manually
python app.py
```

Visit `http://localhost:5000` to access the application.

## ⚙️ **Configuration**

### **Required Environment Variables**

| Variable | Description | Example |
|----------|-------------|---------|
| `SECRET_KEY` | Flask secret key | `secrets.token_hex(32)` |
| `MONGO_URI` | MongoDB connection string | `mongodb+srv://user:pass@cluster.mongodb.net/` |
| `PINECONE_API_KEY` | Pinecone AI service key | `your-pinecone-api-key` |
| `DB_NAME` | Primary database name | `pslvnews` |
| `NEWS_DB_NAME` | News database name | `newsai_db` |

### **Optional Environment Variables**

| Variable | Description | Default |
|----------|-------------|---------|
| `ASSISTANT_NAME` | Pinecone assistant name | `news` |
| `GROQ_API_KEY` | Groq AI service key | `None` |
| `NEWS_API_KEY` | News API service key | `None` |
| `JWT_SECRET_KEY` | JWT authentication key | `SECRET_KEY` |
| `FLASK_ENV` | Flask environment | `development` |
| `DEBUG` | Debug mode | `True` |

## 🚀 **Deployment**

### **Using Docker**
```bash
# Build the Docker image
docker build -t news_app .

# Run with docker-compose
docker-compose up -d
```

### **Using Heroku**
```bash
# Install Heroku CLI
# Login to Heroku
heroku login

# Create Heroku app
heroku create your-app-name

# Set environment variables
heroku config:set SECRET_KEY=your-secret-key
heroku config:set MONGO_URI=your-mongo-uri
heroku config:set PINECONE_API_KEY=your-pinecone-key

# Deploy
git push heroku main
```

### **Using Gunicorn (Production)**
```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

## 📚 **API Documentation**

### **User Authentication**
- `POST /register` - User registration
- `POST /login` - User login
- `GET /logout` - User logout

### **News Management**
- `GET /user/dashboard/` - User dashboard
- `GET /user/dashboard/<category>` - Category news
- `GET /user/dashboard/search` - Search news
- `POST /user/news-analysis/analyze` - Analyze news text

### **Admin Features**
- `GET /admin/` - Admin dashboard
- `GET /admin/news` - Manage news
- `GET /admin/users` - Manage users
- `GET /admin/sources` - Manage news sources

### **Reporter Features**
- `GET /reporter/` - Reporter dashboard
- `POST /reporter/submission` - Submit news
- `POST /reporter/upload` - Upload media files

## 🔧 **Development**

### **Running Tests**
```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=.
```

### **Database Operations**
```bash
# Setup search indexes
python setup_search_indexes.py --setup

# Reset database
python -c "from pymongo import MongoClient; client.drop_database('pslvnews')"
```

### **Code Quality**
```bash
# Format code
black .

# Sort imports
isort .

# Lint code
flake8 .

# Type checking
mypy .
```

## 🛡️ **Security**

- **Secure password hashing** with Flask-Bcrypt
- **Environment variable protection** for sensitive data
- **Input validation** and sanitization
- **SQL injection prevention** with MongoDB
- **CSRF protection** with Flask-WTF
- **Rate limiting** for API endpoints
- **Secure session management**

## 🤝 **Contributing**

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** your changes (`git commit -m 'Add some AmazingFeature'`)
4. **Push** to the branch (`git push origin feature/AmazingFeature`)
5. **Open** a Pull Request

### **Development Guidelines**
- Follow **PEP 8** style guidelines
- Write **comprehensive tests** for new features
- Update **documentation** for API changes
- Use **meaningful commit messages**
- Add **type hints** where applicable

## 🙏 **Acknowledgments**

- **Flask** framework for the web application
- **MongoDB** for data storage
- **Pinecone** for AI-powered features
- **OpenAI** for language models
- **Contributors** and the open-source community

**Made with ❤️ using Flask, MongoDB, and AI**
