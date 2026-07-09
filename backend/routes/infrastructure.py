from fastapi import APIRouter

from config import DATA_API_BASE, REDIS_URL, USE_MOCK

router = APIRouter()

REQUIRED_LINUX_SERVICES = [
    "Redis broker/cache",
    "Celery workers",
    "Celery Beat scheduler",
    "Playwright browser workers",
    "Prometheus metrics",
    "Grafana dashboards",
]


@router.get("/infrastructure/status")
def infrastructure_status():
    return {
        "mock_mode": USE_MOCK,
        "data_api_configured": bool(DATA_API_BASE),
        "data_api_base": DATA_API_BASE or None,
        "redis_configured": bool(REDIS_URL),
        "vercel_supported": False,
        "message": "Live scraping and scheduled analysis require a Linux worker stack. Vercel can host the frontend/API shell, but not Redis, Celery workers, Celery Beat, Playwright browsers, Prometheus, or Grafana as long-running services.",
        "required_linux_services": REQUIRED_LINUX_SERVICES,
    }
