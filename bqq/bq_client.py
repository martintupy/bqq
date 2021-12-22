from google.cloud.bigquery import Client

from bqq.util.spinner import Spinner


class BqClient:
    def __init__(self):
        self._client = None

    @property
    def client(self):
        if not self._client:
            with Spinner():
                self._client = Client()
        return self._client
