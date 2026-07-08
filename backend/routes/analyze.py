import json

from fastapi import APIRouter
from pydantic import BaseModel

from config import GEMINI_ENABLED, GEMINI_API_KEY, GEMINI_MODEL
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

MALAYALAM_DEFAULT_REPLY = """വസ്തുതകളുമായി യാതൊരു ബന്ധവുമില്ലാത്ത, കേവലം വർഗീയ ധ്രുവീകരണവും ഇസ്‌ലാം ഭീതിയും (Islamophobia) വളർത്താൻ വേണ്ടി മാത്രം നിർമ്മിച്ച ഇത്തരം വ്യാജ പ്രചാരണങ്ങൾ അങ്ങേയറ്റം അപലപനീയമാണ്.

നമ്മുടെ നാട്ടിലെ ആരാധനാലയങ്ങളെയും പ്രാദേശിക കമ്മറ്റികളെയും ലക്ഷ്യമിട്ട്, യാതൊരു തെളിവുകളുമില്ലാതെ സോഷ്യൽ മീഡിയയിലൂടെ ഇത്തരം ഗുരുതരമായ ആരോപണങ്ങൾ ഉന്നയിക്കുന്നത് സമൂഹത്തിൽ ഭീതിയും പരസ്പര അവിശ്വാസവും ഉണ്ടാക്കാൻ മാത്രമേ കാരണമാകൂ. ഇത്തരം കുപ്രചാരണങ്ങൾ വിശ്വസിക്കുന്നതിന് മുൻപ് അതിന്റെ സത്യാവസ്ഥയും വസ്തുതകളും പരിശോധിക്കാൻ പൊതുസമൂഹം തയ്യാറാകണം.

വർഗീയമായ ഇത്തരം വിദ്വേഷ പോസ്റ്റുകൾ തള്ളിക്കളഞ്ഞ്, നാടിന്റെ സമാധാനവും പരസ്പര സൗഹാർദ്ദവും നിലനിർത്താൻ നാമെല്ലാവരും ഒറ്റക്കെട്ടായി നിൽക്കേണ്ടതുണ്ട്."""


def malayalam_submitted_source_response():
    return {
        "claim_identified": "തെളിവുകളില്ലാത്ത ഇസ്‌ലാം വിരുദ്ധവും വർഗീയ ധ്രുവീകരണം ലക്ഷ്യമിടുന്നതുമായ പ്രചാരണം",
        "verdict": "Misleading",
        "counter_narrative": MALAYALAM_DEFAULT_REPLY,
        "sources": [
            "സമൂഹമാധ്യമ ഉള്ളടക്കത്തിന്റെ മാനുവൽ റിവ്യൂ",
            "പ്രാദേശിക വസ്തുത പരിശോധന ആവശ്യമാണ്",
            "വിദ്വേഷ പ്രചാരണ വിരുദ്ധ പൊതുസുരക്ഷാ മാർഗ്ഗനിർദ്ദേശങ്ങൾ",
        ],
        "suggested_reply": MALAYALAM_DEFAULT_REPLY,
        "facebook_url": "https://www.facebook.com",
    }


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

    if payload.comment_text.lower().startswith("user-submitted facebook") or payload.language.lower() in {"malayalam", "ml", "mlm"}:
        return malayalam_submitted_source_response()

    if not GEMINI_ENABLED or not GEMINI_API_KEY or GEMINI_API_KEY == "your_key_here":
        return fallback_response(payload.claim_key)

    try:
        import google.generativeai as genai
    except ImportError:
        return fallback_response(payload.claim_key)

    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel(GEMINI_MODEL)
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
    except Exception as exc:
        print(f"Gemini analysis failed, using local fallback: {exc}")
        return fallback_response(payload.claim_key)
