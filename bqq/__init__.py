import os
from typing import Optional, Tuple

import click
from google.cloud.bigquery import Client

from bqq.infos import Infos
from bqq.results import Results
from bqq.service.bq_service import BqService
from bqq.service.info_service import InfoService
from bqq.types import JobInfo
from bqq.util import bash_util


@click.command()
@click.argument("sql", required=False)
@click.option("-f", "--file", help="File containing SQL", type=click.File("r"))
@click.option("-y", "--yes", help="Automatic yes to prompt", is_flag=True)
@click.option("-h", "--history", help="Search history", is_flag=True)
@click.option("-d", "--delete", help="Delete job from history", is_flag=True)
@click.option("--clear", help="Clear history", is_flag=True)
@click.option("--sync", help="Sync history from cloud", is_flag=True)
def cli(sql: str, file: str, yes: bool, history: bool, delete: bool, clear: bool, sync: bool):
    """BiqQuery query."""
    job_info = None
    infos = Infos()
    results = Results()
    bq_service = BqService(infos, results)
    info_service = InfoService(infos)
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
        job_info = info_service.search_one()
    elif delete:
        infos = info_service.search()
        click.echo("\n".join([info.job_id for info in infos]))
        if click.confirm(f"Delete selected from history ?", default=True):
            ctx = click.get_current_context()
            bq_service.delete_jobs(infos)
            ctx.exit()
    elif clear:
        ctx = click.get_current_context()
        size = len(infos.get_all())
        if click.confirm(f"Clear history ({size})?", default=False):
            infos.clear()
            results.clear()
            click.echo("All past results cleared")
        ctx.exit()
    elif sync:
        bq_service.sync_history()
    else:
        ctx = click.get_current_context()
        click.echo(ctx.get_help())
        ctx.exit()
    if job_info:
        result = results.read(job_info)
        if not result and click.confirm("Download result ?"):
            bq_service.download_result(job_info.job_id)
            result = results.read(job_info)
        sections = [
            info_service.get_info(job_info),
            info_service.get_sql(job_info),
            result,
        ]
        message = "\n".join(filter(None, sections))
        if bash_util.use_less(message):
            os.environ["LESS"] += " -S"  # enable horizontal scrolling for less
            click.echo_via_pager(message)
        else:
            click.echo(message)
        