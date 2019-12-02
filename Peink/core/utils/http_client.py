import requests
import json

class HttpClient:

    def __init__(self, base_url, headers=None):
        self.base_url = base_url
        self.headers = headers if headers else {}
        self.headers.update({
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        })

    def _url(self, path):
        return "{base_url}{path}".format(
            base_url=self.base_url,
            path=path
        )

    def get(self, path, params=None):
        response = requests.get(
            url=self._url(path),
            params=params,
            headers=self.headers,
        )
        return response.json()

    def post(self, path, params=None, body=None):
        response = requests.post(
            url=self._url(path),
            data=json.dumps(body),
            params=params,
            headers=self.headers
        )
        return response.json()
