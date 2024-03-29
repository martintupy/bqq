from datetime import datetime, timedelta
from typing import List

from google.cloud.bigquery import Client
from google.cloud.bigquery.job.query import QueryJob
from google.oauth2.credentials import Credentials
from rich.console import Console
from rich.progress import Progress, TextColumn, TimeElapsedColumn
from rich.text import Text

from bqq import const
from bqq.config import Config


class BqClient:
    def __init__(self, console: Console, config: Config):
        self._client = None
        self.console = console
        self.config = config

    @property
    def client(self) -> Client:
        if not self._client:
            with self.console.status(Text("Connecting to the API", style=const.darker_style), spinner="point"):
                self._client = Client(
                    project=self.config.project,
                    credentials=Credentials.from_authorized_user_info(self.config.credentials),
                )
        return self._client

    def list_query_jobs(self) -> List[QueryJob]:
        client = self.client
        query_jobs = []
        size = 0
        with Progress(
            TextColumn("[progress.description]{task.description}", style=const.info_style),
            "•",
            TextColumn("[progress.completed]{task.completed}"),
            "•",
            TimeElapsedColumn(),
            console=self.console,
        ) as progress:
            task = progress.add_task("Listing query jobs")
            days_ago = datetime.utcnow() - timedelta(days=self.config.history_days)
            for job in client.list_jobs(min_creation_time=days_ago, state_filter="DONE"):
                if isinstance(job, QueryJob):
                    query_jobs.append(job)
                    progress.advance(task)
                    size += 1
        return query_jobs

    def list_projects(self) -> List[str]:
        size = 0
        projects = []
        client = self.client
        with Progress(
            TextColumn("[progress.description]{task.description}", style=const.info_style),
            "•",
            TextColumn("[progress.completed]{task.completed}"),
            "•",
            TimeElapsedColumn(),
            console=self.console,
        ) as progress:
            task = progress.add_task("Listing available projects")
            for project in client.list_projects():
                projects.append(project.project_id)
                progress.advance(task)
                size += 1
        return projects
