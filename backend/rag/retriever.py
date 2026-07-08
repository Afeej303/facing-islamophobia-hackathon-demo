import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
KB_PATH = BASE_DIR / "knowledge_base.json"

_entries = []


def load_knowledge_base():
    global _entries
    with KB_PATH.open(encoding="utf-8") as file:
        _entries = json.load(file)


def get_entry(claim_key: str):
    if not _entries:
        load_knowledge_base()
    for entry in _entries:
        if entry["key"] == claim_key:
            return entry
    return None


def retrieve(query: str, claim_key: str | None = None, n: int = 2):
    if not _entries:
        load_knowledge_base()
    keyed = get_entry(claim_key) if claim_key else None
    entries = [keyed] if keyed else []
    query_terms = set(query.lower().split())
    ranked = sorted(
        [entry for entry in _entries if entry not in entries],
        key=lambda entry: len(query_terms.intersection((entry["claim"] + " " + entry["facts"]).lower().split())),
        reverse=True,
    )
    entries.extend(ranked[: max(0, n - len(entries))])
    return [entry for entry in entries if entry]


def format_context(entries):
    chunks = []
    for entry in entries:
        chunks.append(
            f"Claim: {entry['claim']}\nFacts: {entry['facts']}\nSources: {', '.join(entry['sources'])}"
            + (f"\nReference: {entry['quran_ref']}" if entry.get("quran_ref") else "")
        )
    return "\n\n".join(chunks)
