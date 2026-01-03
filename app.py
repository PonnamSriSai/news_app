import os
from flask import Flask, render_template, request, redirect, url_for, jsonify, session, redirect
from pymongo import MongoClient
from flask_bcrypt import Bcrypt
from bson import ObjectId
from datetime import datetime
from pinecone import Pinecone
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import admin blueprint
from admin import admin_bp

# Import reporter blueprint
from reporter import reporter_bp

app = Flask(__name__)
bcrypt = Bcrypt(app)

# Load configuration from environment variables
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'fallback-secret-key-change-me')
PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
ASSISTANT_NAME = os.getenv('ASSISTANT_NAME', 'news')

# Validate required environment variables
if not PINECONE_API_KEY:
    raise ValueError("PINECONE_API_KEY environment variable is required")

pc = Pinecone(api_key=PINECONE_API_KEY)

assistant = pc.assistant.Assistant(
    assistant_name=ASSISTANT_NAME
)
# Register admin blueprint
app.register_blueprint(admin_bp)

# Register reporter blueprint
app.register_blueprint(reporter_bp)

# MongoDB connection using environment variables
MONGO_URI = os.getenv('MONGO_URI')
DB_NAME = os.getenv('DB_NAME', 'pslvnews')
NEWS_DB_NAME = os.getenv('NEWS_DB_NAME', 'newsai_db')

if not MONGO_URI:
    raise ValueError("MONGO_URI environment variable is required")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
news_db = client[NEWS_DB_NAME]  # Separate database for news data
users = db.users

@app.route("/")
def hello_world():
    return render_template("index.html")

@app.route("/user/dashboard/")
def user_dashboard():
    return redirect(url_for("user_dashboard_category", category="breakingnews"))


@app.route("/user/chatbot")
def user_chatbot():
    return render_template("user_chatbot.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message")

    if not user_message:
        return jsonify({"error": "Empty message"}), 400

    response = assistant.chat(
        messages=[
            {"role": "user", "content": user_message}
        ]
    )

    reply = response["message"]["content"]

    return jsonify({"reply": reply})

@app.route("/user/for_you")
def user_for_you():
    category = "breakingnews"
    try:
        # Default category
        if not category or category.strip() == "":
            return redirect(url_for("user_dashboard"))

        if category == "breakingnews":
            news_list = list(
                news_db.today_breaking_priority
                .find()
                .sort("publishedAt", -1)
            )
        else:
            # Fetch news by category from MongoDB
            news_list = list(
                news_db.news_master
                .find({"category": category})
                .sort("created_at", -1)
            )

        # Convert ObjectId to string for template usage
        for news in news_list:
            news["_id"] = str(news["_id"])

        print(f"Loaded {len(news_list)} news for category: {category}")
        # print(news_list)
        # Render dashboard with news data
        return render_template(
            "for_you.html",
            selected_category=category,
            news_list=news_list,
            news_count=len(news_list)
        )

    except Exception as e:
        print("Error loading dashboard:", e)
        return render_template(
            "user_dashboard.html",
            selected_category=category,
            news_list=[],
            news_count=0,
            error="Failed to load news"
        )


@app.route("/user/dashboard/<category>", methods=["GET"])
def user_dashboard_category(category):
    try:
        # Default category
        if not category or category.strip() == "":
            return redirect(url_for("user_dashboard"))

        if category == "breakingnews":
            news_list = list(
                news_db.today_breaking_priority
                .find()
                .sort("publishedAt", -1)
            )
        else:
            # Fetch news by category from MongoDB
            news_list = list(
                news_db.news_master
                .find({"category": category})
                .sort("created_at", -1)
            )

        # Convert ObjectId to string for template usage
        for news in news_list:
            news["_id"] = str(news["_id"])

        print(f"Loaded {len(news_list)} news for category: {category}")
        # print(news_list)
        # Render dashboard with news data
        return render_template(
            "user_dashboard.html",
            selected_category=category,
            news_list=news_list,
            news_count=len(news_list)
        )

    except Exception as e:
        print("Error loading dashboard:", e)
        return render_template(
            "user_dashboard.html",
            selected_category=category,
            news_list=[],
            news_count=0,
            error="Failed to load news"
        )

@app.route("/user/dashboard/search", methods=["GET"])
def search_news():
    try:
        # Get search query from URL parameters
        query = request.args.get('q', '').strip()
        
        # Validate search query
        if not query:
            return render_template(
                "user_dashboard.html",
                selected_category="search",
                news_list=[],
                news_count=0,
                search_query="",
                search_results=True,
                error="Please enter a search term"
            )
        
        # Limit query length to prevent abuse
        if len(query) > 100:
            query = query[:100]
            search_truncated = True
        else:
            search_truncated = False
        
        news_list = []
        search_method = "regex"  # Default search method
        
        # Try text search first (more efficient with indexes)
        try:
            news_list = list(
                news_db.news_master
                .find(
                    {"$text": {"$search": query}},
                    {"score": {"$meta": "textScore"}}
                )
                .sort([("score", {"$meta": "textScore"})])
                .limit(50)  # Limit results for performance
            )
            search_method = "text"
            print(f"Text search for '{query}' returned {len(news_list)} results")
        except Exception as text_search_error:
            print(f"Text search failed: {text_search_error}, falling back to regex search")
            
            # Fallback to regex search if text search fails
            news_list = list(
                news_db.news_master
                .find({
                    "$or": [
                        {"title": {"$regex": query, "$options": "i"}},
                        {"description": {"$regex": query, "$options": "i"}},
                        {"full_text": {"$regex": query, "$options": "i"}},
                        {"content": {"$regex": query, "$options": "i"}},
                        {"category": {"$regex": query, "$options": "i"}}
                    ]
                })
                .sort("created_at", -1)
                .limit(50)  # Limit results for performance
            )
            search_method = "regex"
            print(f"Regex search for '{query}' returned {len(news_list)} results")
        
        # Convert ObjectId to string for template usage
        for news in news_list:
            news["_id"] = str(news["_id"])
        
        # Add search method info to template context
        return render_template(
            "user_dashboard.html",
            selected_category="search",
            news_list=news_list,
            news_count=len(news_list),
            search_query=query,
            search_results=True,
            search_truncated=search_truncated,
            search_method=search_method
        )
        
    except Exception as e:
        print("Error during search:", e)
        return render_template(
            "user_dashboard.html",
            selected_category="search",
            news_list=[],
            news_count=0,
            search_query=query if 'query' in locals() else "",
            search_results=True,
            error="Search failed. Please try again."
        )

@app.route("/register", methods = ["GET", "POST"])
def register():
    if request.method == 'POST':
        try:
            user_data = {
                "first_name": request.form.get("first_name"),
                "last_name": request.form.get("last_name"),
                "email": request.form.get("email"),
                "age": int(request.form.get("age")),
                "location": request.form.get("location"),
                "role": request.form.get("role", "user"),  # Default to user role
                "hashed_password": bcrypt.generate_password_hash(
                    request.form.get("password")
                ).decode('utf-8'),
                "created_at": datetime.now(),
                "category_preferences": {},
                "liked_articles": [],
                "shared_articles": [],
                "reading_history": []
            }

            # Check if email already exists
            existing_user = users.find_one({"email": user_data["email"]})
            if existing_user:
                return render_template("register.html", error="Email already registered")

            # Insert into MongoDB
            result = users.insert_one(user_data)
            
            if result.inserted_id:
                return redirect(url_for('login'))
            else:
                return render_template("register.html", error="Registration failed")
                
        except Exception as e:
            print(f"Registration error: {e}")
            return render_template("register.html", error="Registration failed. Please try again.")
        
    return render_template("register.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    # 🔹 GET → show login page (or modal container)
    if request.method == 'GET':
        return render_template('login.html')
        # If login is only a modal, you can also just return ""

    # 🔹 POST → handle login submission (AJAX)
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")

        if not email or not password:
            return jsonify(success=False, message="Missing credentials")

        user = users.find_one({"email": email})
        if not user:
            return jsonify(success=False, message="User not found")

        # Check if using new schema (hashed_password) or old schema (password)
        password_field = "hashed_password" if "hashed_password" in user else "password"
        
        if not bcrypt.check_password_hash(user[password_field], password):
            return jsonify(success=False, message="Invalid password")

        # Set session
        session['user_id'] = str(user['_id'])
        session['user_role'] = user.get('role', 'user')
        session['user_name'] = f"{user.get('first_name', '')} {user.get('last_name', '')}".strip()

        # Redirect users based on role
        user_role = user.get('role', 'user')
        if user_role == 'admin':
            return redirect(url_for('admin.admin_dashboard'))
        elif user_role == 'news_reporter':
            return redirect(url_for('reporter.reporter_dashboard'))
        else:
            return redirect(url_for('user_dashboard_category', category = "breakingnews"))


@app.route('/user/news-analysis', methods=['GET'])
def news_analysis():
    """Render news analysis UI"""
    return render_template('news_analysis.html')

@app.route('/user/news-analysis/analyze', methods=['POST'])
def analyze_news():
    """Analyze news text without saving to database"""
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({'success': False, 'error': 'No text provided'}), 400
        
        news_text = data['text'].strip()
        if not news_text:
            return jsonify({'success': False, 'error': 'Empty text provided'}), 400
        
        # Limit text length to prevent abuse
        if len(news_text) > 5000:
            news_text = news_text[:5000]
        
        # Import analysis functions
        import sys
        import os
        sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))
        from reporter_ingest import run_agent, get_sentiment, remove_emojis
        
        # Clean the text
        clean_text = remove_emojis(news_text)
        
        # Get sentiment analysis
        sentiment_data = get_sentiment(clean_text)
        
        # Get AI analysis
        agent_data, evidence_sources = run_agent(clean_text)
        
        # Prepare response data
        analysis_result = {
            'title': agent_data.get('headline', clean_text[:50] + '...' if len(clean_text) > 50 else clean_text),
            'summary': agent_data.get('summary', clean_text),
            'credibility': agent_data.get('credibility', 0.5),
            'fake_prob': agent_data.get('fake_prob', 0.5),
            'sentiment': sentiment_data['sentiment'],
            'status': 'analyzed',
            'category': agent_data.get('category', 'general'),
            'evidence_sources': evidence_sources
        }
        
        return jsonify({
            'success': True,
            'result': analysis_result
        })
        
    except Exception as e:
        print(f"Analysis error: {e}")
        return jsonify({
            'success': False,
            'error': f'Analysis failed: {str(e)}'
        }), 500

if __name__ == "__main__":
    app.run(debug = True)
