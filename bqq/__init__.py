import os
from typing import Optional, Tuple

import click
from google.cloud.bigquery import Client

from bqq import info, results
from bqq.service import bq_service, info_service
from bqq.types import JobInfo
from bqq.util import bash_util


@click.command()
@click.argument("sql", required=False)
@click.option("-f", "--file", help="File containing SQL", type=click.File("r"))
@click.option("-y", "--yes", help="Automatic yes to prompt", is_flag=True)
@click.option("-h", "--history", help="Search history", is_flag=True)
@click.option("--clear", help="Clear history", is_flag=True)
def cli(sql: str, file: str, yes: bool, history: bool, clear: bool):
    """BiqQuery query."""
    job_info = None
    if file:
        query = file.read()
        job_info = bq_service.call_api(yes, query)
    elif sql and os.path.isfile(sql):
        file = open(sql, "r")
        query = file.read()
        job_info = bq_service.call_api(yes, query)
    elif sql:
        query = sql
        job_info = bq_service.call_api(yes, query)
    elif history:
        job_info = info_service.search()
    elif clear:
        ctx = click.get_current_context()
        size = len(info.get_all())
        if click.confirm(f"Clear history ({size})?", default=False):
            info.clear()
            results.clear()
            click.echo("All past results cleared")
        ctx.exit()
    else:
        ctx = click.get_current_context()
        click.echo(ctx.get_help())
        ctx.exit()
    if job_info:
        lines = [
            info_service.get_info(job_info),
            info_service.get_sql(job_info),
            results.read(job_info.job_id),
        ]
        message = "\n".join(lines)
        if bash_util.use_less(message):
            os.environ["LESS"] += " -S"  # enable horizontal scrolling for less
            click.echo_via_pager(message)
        else:
            click.echo(message)
