import requests
from ratelimit.config import BEARER_TOKEN

class Request:
    def __init__(self, token: str = BEARER_TOKEN, **kwargs):
        self.headers = {'Authorization': f'Bearer {token}'}
        super().__init__(**kwargs)

    def get(self, url):
        try:
            response = requests.get("{0}".format(url), headers=self.headers)
            return response.json()
        except Exception:
            return []

    def put(self, url, data):
        try:
            response = requests.put("{0}".format(url), headers=self.headers, json=data, )
            return response.json()
        except Exception as exc:
            return exc
