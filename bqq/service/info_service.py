from datetime import datetime, timedelta
from types import resolve_bases
from typing import List, Optional

import click
from bqq import const
from bqq.bq_client import BqClient
from bqq.infos import Infos
from bqq.results import Results
from bqq.service.result_service import ResultService
from bqq.types import JobInfo, SearchLine
from bqq.util import bash_util, bq_util
from google.api_core.exceptions import BadRequest, NotFound
from google.cloud.bigquery.job.query import QueryJob, QueryJobConfig
from tinydb.queries import Query


class InfoService:
    def __init__(self, bq_client: BqClient, result_service: ResultService, infos: Infos) -> None:
        self.infos = infos
        self.bq_client = bq_client
        self.result_service = result_service

    def search(self) -> List[JobInfo]:
        rows = self.infos.get_all()
        choices = []
        for row in rows:
            search_line = SearchLine.from_job_info(row)
            choices.append(search_line.to_line)
        lines = bash_util.fzf(choices, multi=True)
        infos = []
        for line in lines:
            search_line = SearchLine.from_line(line)
            if search_line:
                job_info = next((row for row in rows if row.job_id == search_line.job_id), None)
                infos.append(job_info)
        return infos

    def search_one(self) -> JobInfo:
        rows = self.infos.get_all()
        choices = []
        for row in rows:
            search_line = SearchLine.from_job_info(row)
            choices.append(search_line.to_line)
        lines = bash_util.fzf(choices)
        search_line = next((SearchLine.from_line(line) for line in lines), None)
        job_info = None
        if search_line:
            job_info = next((row for row in rows if row.job_id == search_line.job_id), None)
        return job_info

    def sync_infos(self):
        days_ago = datetime.utcnow() - timedelta(days=const.HISTORY_DAYS)
        jobs = self.bq_client.client.list_jobs(min_creation_time=days_ago, state_filter="DONE")
        with click.progressbar(jobs, label="Syncing jobs information") as js:
            for job in js:
                if isinstance(job, QueryJob):
                    job_info = JobInfo.from_query_job(job)
                    self.infos.upsert(job_info)

    def dry_run(self, query: str) -> Optional[QueryJob]:
        job_config = QueryJobConfig()
        job_config.dry_run = True
        job = None
        try:
            job = self.bq_client.client.query(query, job_config=job_config)
        except BadRequest as e:
            click.echo(bash_util.hex_color(const.ERROR)(e.message), err=True)
        return job

    def get_info(self, skip: bool, query: str) -> JobInfo:
        job_info = None
        confirmed = skip
        if not skip:
            job = self.dry_run(query)
            if job:
                click.echo(InfoService.get_dry_info_header(job))
                confirmed = click.confirm("Do you want to continue?", default=False)
        if confirmed:
            query_job = self.bq_client.client.query(query)
            self.result_service.write_result(query_job)  # extract result before job info
            job_info = JobInfo.from_query_job(query_job)
            self.infos.insert(job_info)
        return job_info

    def delete_infos(self, jobs: List[JobInfo]):
        for job_info in jobs:
            self.bq_client.client.delete_job_metadata(
                job_id=job_info.job_id, project=job_info.project, location=job_info.location
            )
            self.infos.remove(job_info)
            click.echo(f"Job {job_info.job_id} deleted.")

    @staticmethod
    def get_dry_info_header(job: QueryJob) -> str:
        size = bq_util.size_fmt(job.total_bytes_processed)
        cost = bq_util.price_fmt(job.total_bytes_processed)
        lines = [
            f"{bash_util.hex_color(const.INFO)('Billing project')} = {job.project}",
            f"{bash_util.hex_color(const.INFO)('Estimated size')} = {size}",
            f"{bash_util.hex_color(const.INFO)('Estimated cost')} = {cost}",
        ]
        return "\n".join(lines)

    @staticmethod
    def get_info_header(job_info: JobInfo) -> str:
        cache_hit = "(cache hit)" if job_info.cache_hit else ""
        console_link = bash_util.hex_color(const.LINK)(job_info.google_link)
        lines = [
            f"{bash_util.hex_color(const.INFO)('Creation time')} = {job_info.created_fmt}",
            f"{bash_util.hex_color(const.INFO)('Query cost')} = {job_info.price_fmt} {cache_hit}",
            f"{bash_util.hex_color(const.INFO)('Slot time')} = {job_info.slot_time}",
            f"{bash_util.hex_color(const.INFO)('Console link')} = {console_link}",
        ]
        return "\n".join(lines)

    @staticmethod
    def get_sql(job_info: JobInfo) -> str:
        return bash_util.color_keywords(job_info.query)
