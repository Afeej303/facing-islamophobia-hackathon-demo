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
FB_APP_ID=your_meta_app_id
FB_APP_SECRET=your_meta_app_secret
FB_GRAPH_VERSION=v20.0
FB_REDIRECT_URI=http://127.0.0.1:8000/api/facebook/callback
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
2. Add this OAuth redirect URI in the Meta dashboard:

```bash
http://127.0.0.1:8000/api/facebook/callback
```

3. Request the minimum Page permissions used by the demo:

```bash
pages_show_list
pages_read_engagement
pages_read_user_content
pages_manage_engagement
```

4. Put `FB_APP_ID` and `FB_APP_SECRET` in `backend/.env`.
5. Restart the backend and click `Connect account` in the Shield panel.

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
