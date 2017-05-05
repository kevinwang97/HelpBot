import requests
from datetime import datetime
from datetime import timedelta

_DEFAULT_BASE_URL = "https://api.yelp.com"


class YelpClient():
    def __init__(self, key=None, retry_timeout=60, queries_per_second=10):
        self.key = key
        self.retry_timeout = timedelta(seconds=retry_timeout)
        self.queries_per_second = queries_per_second

    def request(self, url, params):