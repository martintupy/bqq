from typing import Optional

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
    q = client.query(query)
    result = q.result()
    job_id = q.job_id
    project = q.project
    location = q.location
    created = q.created
    bytes_billed = q.total_bytes_billed
    cache_hit = q.cache_hit
    header = [field.name for field in result.schema]
    rows = list(result)
    job_info = JobInfo(created, query, project, location, job_id, bytes_billed, cache_hit)
    info.insert(job_info)
    results.write(job_id, header, rows)
    return job_info


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
