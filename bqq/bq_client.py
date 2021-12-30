from google.cloud.bigquery import Client
from rich.console import Console
from bqq import const


class BqClient:
    def __init__(self, console: Console):
        self._client = None
        self.console = console

    @property
    def client(self):
        if not self._client:
            with self.console.status("Connecting to API", spinner="point", spinner_style=const.info_style) as status:
                self._client = Client()
        return self._client
