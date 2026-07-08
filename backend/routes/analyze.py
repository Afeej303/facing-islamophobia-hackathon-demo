import json

from fastapi import APIRouter
from pydantic import BaseModel

from config import GEMINI_API_KEY
from rag.retriever import format_context, get_entry, retrieve

router = APIRouter()


class AnalyzeRequest(BaseModel):
    comment_text: str
    claim_key: str
    language: str = "english"


PROMPT_TEMPLATE = """You are a fact-checker countering Islamophobic misinformation in Indian contexts.
You respond with calm, factual, well-sourced counter-narratives.
You never use aggressive or confrontational language.
You cite real sources: census data, court judgments, academic research, Quranic verses where relevant.

Context from knowledge base:
{retrieved_context}

Islamophobic comment to counter:
"{comment_text}"

Respond in JSON with these exact keys:
- claim_identified: one sentence naming the specific false claim
- verdict: one of "False", "Misleading", "Missing Context"
- counter_narrative: 3-4 sentences with factual rebuttal and sources named inline
- sources: array of 2-3 real source names
- suggested_reply: a calm, shareable social media reply under 100 words

Language: {language}
Respond only in valid JSON. No markdown, no backticks.
"""


def fallback_response(claim_key: str):
    entry = get_entry(claim_key)
    if not entry:
        entry = retrieve("", claim_key=None, n=1)[0]
    sources = entry["sources"][:3]
    return {
        "claim_identified": entry["claim"],
        "verdict": "Misleading",
        "counter_narrative": f"{entry['facts']} Sources commonly cited for this issue include {', '.join(sources)}. The claim needs context and should not be used to target a religious community.",
        "sources": sources,
        "suggested_reply": f"The available evidence does not support this claim. Sources such as {sources[0]} and {sources[1]} give important context and show why fear-based generalizations harm public discussion.",
        "facebook_url": "https://www.facebook.com",
    }


@router.post("/analyze")
def analyze_comment(payload: AnalyzeRequest):
    entries = retrieve(payload.comment_text, payload.claim_key, n=2)
    retrieved_context = format_context(entries)

    if not GEMINI_API_KEY or GEMINI_API_KEY == "your_key_here":
        return fallback_response(payload.claim_key)

    try:
        import google.generativeai as genai
    except ImportError:
        return fallback_response(payload.claim_key)

    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = PROMPT_TEMPLATE.format(
        retrieved_context=retrieved_context,
        comment_text=payload.comment_text,
        language=payload.language,
    )
    response = model.generate_content(prompt)
    text = response.text.strip()
    if text.startswith("```"):
        text = text.strip("`").replace("json", "", 1).strip()
    data = json.loads(text)
    data["facebook_url"] = "https://www.facebook.com"
    return data
