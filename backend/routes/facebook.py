import json
import secrets
from urllib.parse import urlencode
from urllib.request import urlopen

from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse

from config import FB_APP_ID, FB_APP_SECRET, FB_GRAPH_VERSION, FB_REDIRECT_URI

router = APIRouter()

SCOPES = [
    "pages_show_list",
    "pages_read_engagement",
    "pages_read_user_content",
    "pages_manage_engagement",
]

_oauth_states = set()
_connection = {
    "connected": False,
    "pages": [],
}


def facebook_configured():
    return bool(FB_APP_ID and FB_APP_SECRET)


def graph_get(path: str, params: dict):
    url = f"https://graph.facebook.com/{FB_GRAPH_VERSION}/{path}?{urlencode(params)}"
    with urlopen(url, timeout=20) as response:
        return json.loads(response.read().decode("utf-8"))


@router.get("/facebook/status")
def facebook_status():
    return {
        "configured": facebook_configured(),
        "connected": _connection["connected"],
        "pages": _connection["pages"],
        "required_env": ["FB_APP_ID", "FB_APP_SECRET", "FB_REDIRECT_URI"],
        "permissions": SCOPES,
    }


@router.get("/facebook/login-url")
def facebook_login_url():
    if not facebook_configured():
        return {
            "configured": False,
            "message": "Set FB_APP_ID and FB_APP_SECRET in backend/.env, then restart the backend.",
            "required_permissions": SCOPES,
        }

    state = secrets.token_urlsafe(24)
    _oauth_states.add(state)
    query = urlencode(
        {
            "client_id": FB_APP_ID,
            "redirect_uri": FB_REDIRECT_URI,
            "state": state,
            "scope": ",".join(SCOPES),
            "response_type": "code",
        }
    )
    return {
        "configured": True,
        "url": f"https://www.facebook.com/{FB_GRAPH_VERSION}/dialog/oauth?{query}",
    }


def callback_page(title: str, message: str):
    return f"""
    <!doctype html>
    <html>
      <head><title>{title}</title></head>
      <body style="font-family: Inter, Arial, sans-serif; margin: 0; background: #f8fafc; color: #1e293b;">
        <main style="max-width: 680px; margin: 72px auto; padding: 32px; background: white; border: 1px solid #e2e8f0; border-radius: 8px;">
          <h1 style="margin-top: 0;">{title}</h1>
          <p style="line-height: 1.6;">{message}</p>
          <p style="line-height: 1.6; color: #64748b;">Return to IslamGuard, open the Shield panel, and click Connect account. Facebook must send you back here with a temporary authorization code.</p>
        </main>
      </body>
    </html>
    """


@router.get("/facebook/callback", response_class=HTMLResponse)
def facebook_callback(
    code: str | None = None,
    state: str | None = None,
    error: str | None = None,
    error_message: str | None = None,
    error_description: str | None = None,
):
    if error or error_message or error_description:
        return callback_page("Facebook connection failed", error_description or error_message or error or "Facebook did not approve the connection.")
    if not code and not state:
        return callback_page("Facebook callback is ready", "This backend route is working, but it was opened directly.")
    if not code or not state or state not in _oauth_states:
        raise HTTPException(status_code=400, detail="Invalid Facebook OAuth callback")

    _oauth_states.discard(state)
    token_payload = graph_get(
        "oauth/access_token",
        {
            "client_id": FB_APP_ID,
            "client_secret": FB_APP_SECRET,
            "redirect_uri": FB_REDIRECT_URI,
            "code": code,
        },
    )
    user_token = token_payload["access_token"]
    pages_payload = graph_get(
        "me/accounts",
        {
            "access_token": user_token,
            "fields": "id,name,access_token,tasks",
        },
    )
    pages = [
        {
            "id": page.get("id"),
            "name": page.get("name"),
            "tasks": page.get("tasks", []),
            "connected": True,
        }
        for page in pages_payload.get("data", [])
    ]
    _connection["connected"] = bool(pages)
    _connection["pages"] = pages

    return """
    <!doctype html>
    <html>
      <head><title>Facebook connected</title></head>
      <body style="font-family: Inter, Arial, sans-serif; padding: 32px;">
        <h1>Facebook connection complete</h1>
        <p>You can close this tab and return to IslamGuard.</p>
      </body>
    </html>
    """
