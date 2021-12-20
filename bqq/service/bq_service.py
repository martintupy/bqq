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
    job_id = q.job_id
    project = q.project
    location = q.location
    created = q.created
    result = q.result()
    header = [field.name for field in result.schema]
    rows = list(result)
    job_info = JobInfo(created, query, project, location, job_id)
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
    return (
        bash_util.hex_color(const.TABLE_HEADER)("Billed project")
        + f" = {job.project}\n"
        + bash_util.hex_color(const.TABLE_HEADER)("Processed size")
        + f" = {size}\n"
        + bash_util.hex_color(const.TABLE_HEADER)("Estimated cost")
        + f" = {cost}"
    )
