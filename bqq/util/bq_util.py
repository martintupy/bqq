from datetime import datetime
from typing import Tuple

import click
from bqq import const, info, results
from bqq.types import JobInfo
from bqq.util import bash_util
from google.api_core.exceptions import BadRequest
from google.cloud.bigquery import Client, QueryJobConfig
from prettytable import PrettyTable


def dry_run(client: Client, query: str):
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


def size_fmt(num):
    for unit in ["B", "KiB", "MiB", "GiB", "TiB", "PiB"]:
        if abs(num) < 1024:
            size = round(num, 1)
            return f"{size} {unit}"
        else:
            num /= 1024


def price_fmt(num):
    tb = num / 1e12
    price = round(tb * 5, 2)
    return f"{price} $"
