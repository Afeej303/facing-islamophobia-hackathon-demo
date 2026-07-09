from prometheus_client import Counter

crawler_runs_total = Counter("islamguard_crawler_runs_total", "Total crawler runs")
flagged_comments_total = Counter("islamguard_flagged_comments_total", "Total flagged comments")
