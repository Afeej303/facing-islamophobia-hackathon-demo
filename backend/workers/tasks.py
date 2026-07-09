import json

from data_sources import redis_client
from workers.playwright_scraper import collect_facebook_sources


def save_json(key: str, value):
    redis_client().set(key, json.dumps(value, ensure_ascii=False))


try:
    from workers.celery_app import celery_app
except ImportError:
    celery_app = None


if celery_app:
    @celery_app.task
    def scan_facebook_sources():
        snapshot = collect_facebook_sources()
        save_json("islamguard:accounts", snapshot["accounts"])
        save_json("islamguard:stats", snapshot["stats"])
        save_json("islamguard:shield_log", snapshot["shield_log"])
        for account_id, comments in snapshot["comments"].items():
            save_json(f"islamguard:comments:{account_id}", comments)
        return {"accounts": len(snapshot["accounts"])}
