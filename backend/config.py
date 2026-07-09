import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env")

def env_bool(name: str, default: str = "false"):
    return os.getenv(name, default).lower() in {"1", "true", "yes", "on"}


USE_MOCK = env_bool("USE_MOCK", "true")
DATA_API_BASE = os.getenv("DATA_API_BASE", "").rstrip("/")
REDIS_URL = os.getenv("REDIS_URL", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_ENABLED = os.getenv("GEMINI_ENABLED", "false").lower() == "true"
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
FB_APP_ID = os.getenv("FB_APP_ID")
FB_APP_SECRET = os.getenv("FB_APP_SECRET")
FB_GRAPH_VERSION = os.getenv("FB_GRAPH_VERSION", "v20.0")
FB_REDIRECT_URI = os.getenv("FB_REDIRECT_URI", "http://127.0.0.1:8000/api/facebook/callback")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://127.0.0.1:5173")
FB_SCOPES = [
    scope.strip()
    for scope in os.getenv("FB_SCOPES", "public_profile").split(",")
    if scope.strip()
]
