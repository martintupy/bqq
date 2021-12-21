from datetime import datetime, timedelta
from typing import List, Optional

import click
from bqq import const, info, results
from bqq.types import JobInfo
from bqq.util import bash_util, bq_util
from google.api_core.exceptions import BadRequest
from google.cloud.bigquery import Client, QueryJobConfig
from google.cloud.bigquery.job.query import QueryJob
from prettytable import PrettyTable


def dry_run(client: Client, query: str) -> Optional[QueryJob]:
    job_config = QueryJobConfig()
    job_config.dry_run = True
    job = None
    try:
        job = client.query(query, job_config=job_config)
    except BadRequest as e:
        click.echo(bash_util.hex_color(const.ERROR)(e.message), err=True)
    return job


def run_query(client: Client, query: str) -> JobInfo:
    query_job = client.query(query)
    write_result(query_job)  # extract result first
    job_info = JobInfo.from_query_job(query_job)
    info.insert(job_info)
    return job_info


def write_result(query_job: QueryJob):
    try:
        result = query_job.result(max_results=const.MAX_ROWS)
        job_id = query_job.job_id
        results.write(query_job.project, job_id, result)
    except BadRequest as e:
        click.echo(bash_util.hex_color(const.ERROR)(e.message), err=True)


def download_result(job_id: str):
    client = Client()
    job = client.get_job(job_id)
    if isinstance(job, QueryJob):
        write_result(job)
    else:
        click.echo("Query job doesn't exist")


def sync_history() -> List[JobInfo]:
    client = Client()
    days_ago = datetime.utcnow() - timedelta(days=const.HISTORY_DAYS)
    jobs = client.list_jobs(min_creation_time=days_ago, state_filter="DONE")
    with click.progressbar(jobs, label="Syncing jobs information") as js:
        for job in js:
            if isinstance(job, QueryJob):
                job_info = JobInfo.from_query_job(job)
                info.upsert(job_info)


def call_api(yes: bool, query: str) -> Optional[JobInfo]:
    client = Client()
    job = dry_run(client, query)
    confirmed = yes
    job_info = None
    if not confirmed and job:
        click.echo(get_header(job))
        confirmed = click.confirm("Do you want to continue?", default=False)
    if confirmed and job:
        job_info = run_query(client, query)
    return job_info


def get_header(job: QueryJob) -> str:
    size = bq_util.size_fmt(job.total_bytes_processed)
    cost = bq_util.price_fmt(job.total_bytes_processed)
    lines = [
        f"{bash_util.hex_color(const.INFO)('Billing project')} = {job.project}",
        f"{bash_util.hex_color(const.INFO)('Estimated size')} = {size}",
        f"{bash_util.hex_color(const.INFO)('Estimated cost')} = {cost}",
    ]
    return "\n".join(lines)
