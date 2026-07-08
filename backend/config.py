import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env")

USE_MOCK = True
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
FB_APP_ID = os.getenv("FB_APP_ID")
FB_APP_SECRET = os.getenv("FB_APP_SECRET")
FB_GRAPH_VERSION = os.getenv("FB_GRAPH_VERSION", "v20.0")
FB_REDIRECT_URI = os.getenv("FB_REDIRECT_URI", "http://127.0.0.1:8000/api/facebook/callback")
