from google.cloud.bigquery import Client
from rich.console import Console


class BqClient:
    def __init__(self, console: Console):
        self._client = None
        self.console = console

    @property
    def client(self):
        if not self._client:
            with self.console.status("Connecting to the API", spinner="point") as status:
                self._client = Client()
        return self._client
