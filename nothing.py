import os
from pymongo import MongoClient
from faker import Faker
from datetime import datetime, timedelta
from bson import ObjectId
import random
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ===================== CONFIG =====================
MONGO_URI = os.getenv('MONGO_URI')
DB_NAME = os.getenv('DB_NAME', 'pslvnews')
COLLECTION_NAME = "news"
TOTAL_NEWS = 1000

if not MONGO_URI:
    raise ValueError("MONGO_URI environment variable is required")
# ==================================================

fake = Faker()

# Allowed categories
categories = [
    "Politics",
    "Technology",
    "Sports",
    "Entertainment",
    "Business",
    "Health",
    "Science",
    "World"
]

# Category → Image mapping (STRICT)
CATEGORY_IMAGES = {
    "Politics": "politics.jpg",
    "Technology": "technology.jpg",
    "Sports": "sports.jpg",
    "Entertainment": "entertainment.jpeg",
    "Business": "buissness.jpeg",
    "Health": "health.jpeg",
    "Science": "science.jpeg",
    "World": "world.jpeg"
}

sentiments = ["positive", "neutral", "negative"]
statuses = ["monitoring", "verified", "flagged"]
sources = ["whatsapp", "twitter", "facebook", "news", "telegram"]

# Mongo connection
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# Date range (1 year including 29 Dec 2025)
today = datetime(2025, 12, 29)
start_date = today - timedelta(days=364)

documents = []

for _ in range(TOTAL_NEWS):
    # Random date within the year
    random_offset = random.randint(0, 364)
    date = start_date + timedelta(days=random_offset)

    category = random.choice(categories)

    published_at = date.replace(
        hour=random.randint(0, 23),
        minute=random.randint(0, 59),
        second=random.randint(0, 59)
    )

    doc = {
        "title": fake.sentence(nb_words=10),
        "content": fake.text(max_nb_chars=180),
        "full_text": fake.paragraph(nb_sentences=8),
        "source": random.choice(sources),
        "publishedAt": published_at.isoformat(),
        "date": date.strftime("%Y-%m-%d"),
        "week": date.isocalendar()[1],
        "month": date.month,
        "year": date.year,
        "category": category,
        "credibility": round(random.uniform(0.6, 0.95), 2),
        "fake_prob": round(random.uniform(0.05, 0.4), 2),
        "summary": fake.text(max_nb_chars=140),
        "time": published_at.strftime("%H:%M:%S"),
        "status": random.choice(statuses),
        "associateMedia": {
            "images": ['images/'+CATEGORY_IMAGES[category]],
            "videos": []
        },
        "location": {
            "district": fake.city(),
            "state": fake.state(),
            "country": "India"
        },
        "sentiment": random.choice(sentiments),
        "reporter_id": str(ObjectId()),
        "reporter_name": fake.name(),
        "created_at": published_at,
        "evidence_sources": [
            {
                "title": fake.sentence(),
                "url": fake.url()
            }
            for _ in range(random.randint(2, 5))
        ]
    }

    documents.append(doc)

# Insert all documents
collection.insert_many(documents)

print(f"✅ Successfully inserted {TOTAL_NEWS} news documents into MongoDB!")

