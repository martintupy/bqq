from datetime import datetime, timedelta
from typing import List, Optional

import click
from bqq import const
from bqq.infos import Infos
from bqq.results import Results
from bqq.types import JobInfo
from bqq.util import bash_util, bq_util
from bqq.util.spinner import Spinner
from google.api_core.exceptions import BadRequest, NotFound
from google.cloud.bigquery import Client, QueryJobConfig
from google.cloud.bigquery.job.query import QueryJob
from prettytable import PrettyTable


class BqService:
    def __init__(self, infos: Infos, results: Results):
        self._client = None
        self.infos = infos
        self.results = results

    @property
    def client(self):
        if not self._client:
            with Spinner():
                self._client = Client()
        return self._client

    @staticmethod
    def get_header(job: QueryJob) -> str:
        size = bq_util.size_fmt(job.total_bytes_processed)
        cost = bq_util.price_fmt(job.total_bytes_processed)
        lines = [
            f"{bash_util.hex_color(const.INFO)('Billing project')} = {job.project}",
            f"{bash_util.hex_color(const.INFO)('Estimated size')} = {size}",
            f"{bash_util.hex_color(const.INFO)('Estimated cost')} = {cost}",
        ]
        return "\n".join(lines)

    def dry_run(self, query: str) -> Optional[QueryJob]:
        job_config = QueryJobConfig()
        job_config.dry_run = True
        job = None
        try:
            job = self.client.query(query, job_config=job_config)
        except BadRequest as e:
            click.echo(bash_util.hex_color(const.ERROR)(e.message), err=True)
        return job

    def run_query(self, query: str) -> JobInfo:
        query_job = self.client.query(query)
        self.write_result(query_job)  # extract result first
        job_info = JobInfo.from_query_job(query_job)
        self.infos.insert(job_info)
        return job_info

    def write_result(self, query_job: QueryJob):
        try:
            result = query_job.result(max_results=const.MAX_ROWS)
            job_id = query_job.job_id
            self.results.write(query_job.project, job_id, result)
        except (BadRequest, NotFound) as e:
            click.echo(bash_util.hex_color(const.ERROR)(e.message), err=True)

    def download_result(self, job_id: str):
        job = self.client.get_job(job_id)
        if isinstance(job, QueryJob):
            self.write_result(job)
        else:
            click.echo("Query job doesn't exist")

    def delete_jobs(self, jobs: List[JobInfo]):
        client = Client()
        for job_info in jobs:
            client.delete_job_metadata(
                job_id=job_info.job_id, project=job_info.project, location=job_info.location
            )
            self.infos.remove(job_info)
            click.echo(f"Job {job_info.job_id} deleted.")

    def sync_history(self) -> List[JobInfo]:
        days_ago = datetime.utcnow() - timedelta(days=const.HISTORY_DAYS)
        jobs = self.client.list_jobs(min_creation_time=days_ago, state_filter="DONE")
        with click.progressbar(jobs, label="Syncing jobs information") as js:
            for job in js:
                if isinstance(job, QueryJob):
                    job_info = JobInfo.from_query_job(job)
                    self.infos.upsert(job_info)

    def call_api(self, yes: bool, query: str) -> Optional[JobInfo]:
        job = self.dry_run(query)
        confirmed = yes
        job_info = None
        if not confirmed and job:
            click.echo(BqService.get_header(job))
            confirmed = click.confirm("Do you want to continue?", default=False)
        if confirmed and job:
            job_info = self.run_query(query)
        return job_info
