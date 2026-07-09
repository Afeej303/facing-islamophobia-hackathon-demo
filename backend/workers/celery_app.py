from celery import Celery

from config import REDIS_URL

broker_url = REDIS_URL or "redis://localhost:6379/0"

celery_app = Celery(
    "islamguard",
    broker=broker_url,
    backend=broker_url,
    include=["workers.tasks"],
)

celery_app.conf.beat_schedule = {
    "scan-facebook-sources-every-15-minutes": {
        "task": "workers.tasks.scan_facebook_sources",
        "schedule": 15 * 60,
    }
}
