import os
from typing import Optional, Tuple

import click
from google.cloud.bigquery import Client

from bqq import const
from bqq.bq_client import BqClient
from bqq.infos import Infos
from bqq.results import Results
from bqq.service.info_service import InfoService
from bqq.service.result_service import ResultService
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
    bq_client = BqClient()
    infos = Infos()
    results = Results()
    result_service = ResultService(bq_client, results)
    info_service = InfoService(bq_client, result_service, infos)
    if file:
        query = file.read()
        job_info = info_service.get_info(yes, query)
    elif sql and os.path.isfile(sql):
        with open(sql, "r") as file:
            query = file.read()
            job_info = info_service.get_info(yes, query)
    elif sql:
        job_info = info_service.get_info(yes, sql)
    elif history:
        job_info = info_service.search_one()
    elif delete:
        infos = info_service.search()
        click.echo("\n".join([info.job_id for info in infos]))
        if click.confirm(f"Delete selected from history ?", default=True):
            ctx = click.get_current_context()
            info_service.delete_infos(infos)
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
        info_service.sync_infos()
    else:
        ctx = click.get_current_context()
        click.echo(ctx.get_help())
        ctx.exit()
    if job_info:
        info_header = info_service.get_info_header(job_info)
        sql = info_service.get_sql(job_info)
        width = bash_util.get_max_width([info_header, sql])
        line = bash_util.hex_color(const.DARKER)("─" * width)
        lines = [
            line,
            info_service.get_info_header(job_info),
            line,
            info_service.get_sql(job_info),
            line,
        ]
        click.echo("\n".join(lines))
        result = results.read(job_info)
        if not result and click.confirm("Download result ?"):
            result_service.download_result(job_info.job_id)
            result = results.read(job_info)
        if result:
            if bash_util.use_less(result):
                os.environ["LESS"] += " -S"  # enable horizontal scrolling for less
                click.echo_via_pager(result)
            else:
                click.echo(result)
