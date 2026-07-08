class FacebookScraper:
    """
    Production scraper using facebook-scraper library or a selenium-based
    approach on Linux. It feeds data to the same API contract as mock.py.
    In demo mode, mock.py is used instead.
    """

    def __init__(self, accounts: list):
        self.accounts = accounts

    def get_flagged_comments(self, account_id: str):
        raise NotImplementedError("Use mock.py for demo mode")

    def get_account_stats(self, account_id: str):
        raise NotImplementedError("Use mock.py for demo mode")
