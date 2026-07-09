def collect_facebook_sources():
    """
    Linux worker entry point.

    In production this runs inside Celery workers with Playwright installed:
      python -m playwright install chromium

    It should collect Facebook post/reel data, normalize it to the public API
    contract, and write snapshots into Redis through workers.tasks.
    """
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        raise RuntimeError("Playwright is required on the Linux worker host.") from exc

    with sync_playwright():
        # Intentionally minimal: the hackathon repo exposes the integration
        # boundary without shipping a brittle Facebook scraper.
        return {
            "accounts": [],
            "comments": {},
            "stats": {
                "total_flagged_today": 0,
                "accounts_monitored": 0,
                "responses_sent": 0,
                "comments_hidden": 0,
            },
            "shield_log": [],
        }
