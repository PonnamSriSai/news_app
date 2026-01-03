import os
import json
from datetime import datetime
from pymongo import MongoClient
from dotenv import load_dotenv
import random

# ================== CONFIG ==================
load_dotenv()

# Optional imports with error handling
try:
    from ddgs import DDGS
    DUCKDUCKGO_AVAILABLE = True
except ImportError:
    DUCKDUCKGO_AVAILABLE = False

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

try:
    from groq import Groq
    GROQ_API_KEY = os.getenv('GROQ_API_KEY')
    if GROQ_API_KEY:
        groq_client = Groq(api_key=GROQ_API_KEY)
        GROQ_AVAILABLE = True
    else:
        GROQ_AVAILABLE = False
        print("Warning: GROQ_API_KEY not found in environment variables")
except ImportError:
    GROQ_AVAILABLE = False

# Load configuration from environment variables
MONGO_URI = os.getenv('MONGO_URI')
NEWS_API_KEY = os.getenv('NEWS_API_KEY')
DB_NAME = os.getenv('NEWS_DB_NAME', 'newsai_db')
MASTER_COL = "news_master"
ANON_COL = "anonymous_news"
LOCAL_DIR = "anonymous_news_local"
os.makedirs(LOCAL_DIR, exist_ok=True)

FAMOUS_SOURCES = ["bbc", "reuters", "the hindu", "cnn", "ndtv", "al jazeera", "times of india"]

# ================== DB ==================
# client = MongoClient(MONGO_URI)
# db = client[DB_NAME]
# news_master = db[MASTER_COL]
# anonymous_news = db[ANON_COL]

# ================== UTIL ==================
def now_utc():
    return datetime.utcnow()

def is_famous(source: str) -> bool:
    return any(f in source.lower() for f in FAMOUS_SOURCES)

import re

def remove_emojis(text):
    """
    Remove emojis and other non-text Unicode characters from input.
    """
    # Emoji pattern (covers most emojis)
    emoji_pattern = re.compile(
        "[" 
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags
        "\U00002702-\U000027B0"
        "\U000024C2-\U0001F251"
        "]+",
        flags=re.UNICODE
    )
    return emoji_pattern.sub(r'', text)


# ================== FREE GEMINI 1.5 API ==================
from textblob import TextBlob

def get_sentiment(text):
    """
    Returns sentiment label and polarity score
    """
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity  # -1 to +1

    if polarity > 0.1:
        label = "positive"
    elif polarity < -0.1:
        label = "negative"
    else:
        label = "neutral"

    return {
        "sentiment": label,
        "sentiment_score": round(polarity, 3)
    }


import json

def analyze_with_gemini_free(text):
    prompt = f"""
You are a news intelligence system and fact checking expert.

Return STRICT JSON only.
No explanation.
No markdown.
No extra text.
Focus more on credibility and fake probability.
its very important to analyze the news as per current news scenario and give credibility and fake probability also gve following details.
based on current news circumstances yo have to give following details.

JSON format:
{{
  "headline": "",
  "summary": "",
  "district": "",
  "state": "",
  "country": "",
  "category": ""
  "credibility": number between 0 and 1,
  "fake_prob": number between 0 and 1
}}

Text:
{text}
"""

    response = groq_client.chat.completions.create(
        model="llama-3.1-8b-instant",   # ✅ FREE + FAST
        messages=[
            {"role": "system", "content": "You output only valid JSON."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    raw = response.choices[0].message.content.strip()

    # --- SAFE JSON EXTRACTION ---
    start = raw.find("{")
    end = raw.rfind("}") + 1

    if start == -1 or end == -1:
        raise ValueError("Groq did not return valid JSON")

    return json.loads(raw[start:end])




# ================== AGENT ==================
def run_agent(full_text: str):
    full_text = remove_emojis(full_text)
    # DuckDuckGo search
    trusted_hits = 0
    evidence_sources = []

    # Only try DuckDuckGo if available
    if DUCKDUCKGO_AVAILABLE:
        try:
            with DDGS() as ddgs:
                results = ddgs.text(full_text, max_results=8)
                for r in results:
                    title = r.get("title", "").lower()
                    link = r.get("href", "").lower()
                    if any(f in title or f in link for f in FAMOUS_SOURCES):
                        trusted_hits += 1
                    evidence_sources.append({"title": r.get("title"), "url": r.get("href")})
        except Exception as e:
            print(f"DuckDuckGo search failed: {e}")

    # NewsAPI search - only try if requests available
    if REQUESTS_AVAILABLE:
        try:
            url = "https://newsapi.org/v2/everything"
            params = {"q": full_text[:200], "apiKey": NEWS_API_KEY, "pageSize": 5}
            res = requests.get(url, params=params).json()
            if res.get("articles"):
                trusted_hits += len(res["articles"])
                for a in res["articles"]:
                    evidence_sources.append({"title": a["title"], "url": a["url"]})
        except Exception as e:
            print(f"NewsAPI search failed: {e}")

    # Use Groq API if available
    if GROQ_AVAILABLE:
        try:
            ai_data = analyze_with_gemini_free(full_text)
            return ai_data, evidence_sources
        except Exception as e:
            print(f"Groq analysis failed: {e}")
    
    # Fallback when APIs are not available
    return {
        "headline": full_text[:50] + "..." if len(full_text) > 50 else full_text,
        "summary": full_text,
        "district": "",
        "state": "",
        "country": "India",
        "category": "general",
        "credibility": 0.5,
        "fake_prob": 0.5
    }, evidence_sources

# ================== INGEST FUNCTION ==================
def ingest_news(full_text, source, district, state, country):
    full_text=remove_emojis(full_text)
    sentiment_data = get_sentiment(full_text)
    created = now_utc()
    agent_data, evidence_sources = run_agent(full_text)

    published_at = now_utc().isoformat()

    if is_famous(source):
        status = "verified"
        credibility = 1.0
        fake_prob = 0.0
    else:
        status = "monitoring"
        credibility = agent_data.get("credibility")
        fake_prob = agent_data.get("fake_prob")

    doc = {
        "title": agent_data.get("headline", full_text[:50]),
        "content": agent_data.get("summary", full_text),
        "full_text": full_text,
        "source": source,
        "publishedAt": published_at,
        "date": published_at[:10],
        "week": datetime.fromisoformat(published_at).isocalendar()[1],
        "month": datetime.fromisoformat(published_at).month,
        "year": datetime.fromisoformat(published_at).year,
        "category": agent_data.get("category", "general"),
        "credibility": credibility,
        "fake_prob": fake_prob,
        "summary": agent_data.get("summary", full_text[:150]),
        "time": published_at[11:19],
        "status": status,
        "associateMedia.images": [],
        "associateMedia.videos": [],
        "location.district": district,
        "location.state": state,
        "location.country": country,
        "sentiment": sentiment_data["sentiment"]
    }


    # master_id = news_master.insert_one(doc).inserted_id
    # doc["_id"] = str(master_id)
    # with open(f"{LOCAL_DIR}/{master_id}.json", "w") as f:
    with open(f"{LOCAL_DIR}/test.json", "w") as f:
        json.dump(doc, f, indent=2, default=str)

    print(f"News stored as {'verified' if status == 'verified' else 'monitoring'}")
    return doc
