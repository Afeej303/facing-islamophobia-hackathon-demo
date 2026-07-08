# IslamGuard

IslamGuard is a hackathon demo for monitoring public Facebook-page comments, identifying Islamophobic narratives, and generating calm, sourced counter-responses for a human moderator to review and post.

The app has two layers:

- A monitoring dashboard for flagged accounts, comments, threat scores, and AI-assisted replies.
- A shield panel for Muslim account owners to review hidden or deleted hateful comments on their own content.

All data is representative mock data except generated counter-responses. If `GEMINI_API_KEY` is present, the backend calls Gemini. Without a key, it returns a local demo response from the knowledge base so the full flow still works.

## Stack

- Frontend: React with Vite
- Backend: Python FastAPI
- AI: Google Gemini API, optional for local demo
- Knowledge base: local JSON retriever with the same route contract expected by a future vector store
- Config: `.env` files

## Setup

Backend:

```bash
cd backend
python -m pip install -r requirements.txt
```

Frontend:

```bash
cd frontend
npm install
```

## Environment

Backend `.env`:

```bash
GEMINI_API_KEY=your_key_here
GEMINI_ENABLED=false
GEMINI_MODEL=gemini-2.0-flash
FB_APP_ID=your_meta_app_id
FB_APP_SECRET=your_meta_app_secret
FB_GRAPH_VERSION=v20.0
FB_REDIRECT_URI=https://your-ngrok-domain.ngrok-free.app/api/facebook/callback
FRONTEND_URL=http://127.0.0.1:5173
FB_SCOPES=public_profile
```

Frontend `.env`:

```bash
VITE_API_BASE=http://localhost:8000/api
```

## Run

Start the backend:

```bash
cd backend
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

On Windows, you can also run:

```bash
start-backend.bat
```

If double-clicking closes too quickly or you want a separate visible terminal:

```bash
open-backend-terminal.bat
```

Start the frontend:

```bash
cd frontend
npm run dev
```

On Windows, you can also run:

```bash
start-frontend.bat
```

To open both app terminals on Windows:

```bash
open-app-terminals.bat
```

The easiest Windows path is:

```bash
START_ISLAMGUARD.bat
```

It opens the backend, opens the frontend, and then opens the Shield panel.

Open the Vite URL shown in the terminal.

## Demo Flow

1. Open the dashboard and review four flagged accounts.
2. Choose the highest-threat account.
3. Open its flagged comments.
4. Generate a counter-response for the demographic replacement comment.
5. Review the claim, verdict, counter narrative, sources, and editable reply.
6. Click `Open Facebook & copy response`.
7. Visit the shield panel and review hidden/deleted comments.
8. Return to the dashboard overview.

## Architecture

The frontend calls only `src/api/client.js`. The backend exposes a stable `/api` contract:

- `GET /api/accounts`
- `GET /api/accounts/{account_id}/comments`
- `GET /api/stats`
- `POST /api/analyze`
- `GET /api/shield/log`
- `POST /api/shield/hide`
- `GET /api/facebook/status`
- `GET /api/facebook/login-url`
- `GET /api/facebook/callback`

In demo mode, `routes/mock.py` provides representative Facebook data. A production scraper can replace that data source while preserving the same frontend contract. `scraper/facebook.py` contains the intended class structure for a later scraper integration.

## Facebook Connection

The Shield panel now has a real OAuth starter flow. To connect a Facebook account:

1. Create a Meta developer app with the Pages API use case.
2. Start the backend on port 8000.
3. In a separate terminal, expose the backend with ngrok:

```bash
ngrok http 8000
```

4. Copy the HTTPS forwarding URL from ngrok, then set the backend redirect URI:

```bash
FB_REDIRECT_URI=https://your-ngrok-domain.ngrok-free.app/api/facebook/callback
```

5. Add that exact same HTTPS redirect URI in the Meta dashboard under valid OAuth redirect URIs.
6. Start with basic Facebook Login while testing:

```bash
FB_SCOPES=public_profile
```

7. After the app is configured for Pages API permissions in Meta, switch to the Page scopes:

```bash
FB_SCOPES=pages_show_list,pages_read_engagement,pages_read_user_content,pages_manage_engagement
```

8. Put `FB_APP_ID`, `FB_APP_SECRET`, `FB_SCOPES`, and the ngrok `FB_REDIRECT_URI` in `backend/.env`.
9. Restart the backend and click `Connect account` in the Shield panel.

Facebook OAuth requires a secure HTTPS redirect URL. Plain `http://127.0.0.1:8000/api/facebook/callback` can be useful for local route testing, but Facebook may block it for login. For the hackathon demo, ngrok is the fastest reliable option. Self-signed local SSL is not recommended because Facebook needs a publicly reachable trusted HTTPS URL.

If Facebook says the Page scopes are invalid, keep `FB_SCOPES=public_profile` for the demo login proof. Page permissions require the correct Meta app setup and may require app review or a tester/developer account before Facebook accepts them.

The callback exchanges the OAuth code for a user token, requests managed Pages from `/me/accounts`, and keeps the connected Page list in memory for the demo session. Tokens are not written to disk.

## Extending The Knowledge Base

Add entries to `backend/rag/knowledge_base.json` with:

- `key`
- `claim`
- `facts`
- `sources`
- `quran_ref`

Comments returned from the mock or future scraper should include a matching `claim_key`.

## Note

Real-time scraping pipeline pending platform API access. Demo uses representative data to showcase the full application flow.
