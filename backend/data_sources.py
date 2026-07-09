import json
from typing import Any

from config import REDIS_URL


class DataSourceUnavailable(RuntimeError):
    pass


def redis_client():
    if not REDIS_URL:
        raise DataSourceUnavailable("REDIS_URL is not configured.")
    try:
        import redis
    except ImportError as exc:
        raise DataSourceUnavailable("Install redis support with requirements-linux.txt.") from exc
    return redis.from_url(REDIS_URL, decode_responses=True)


def redis_json(key: str) -> Any:
    client = redis_client()
    value = client.get(key)
    if not value:
        raise DataSourceUnavailable(f"Redis key {key} is empty.")
    return json.loads(value)
