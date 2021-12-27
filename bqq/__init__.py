import json
import os
import subprocess
from pathlib import Path
from typing import Optional, Tuple

import click
from google.cloud.bigquery import Client

from bqq import const, output
from bqq.bq_client import BqClient
from bqq.infos import Infos
from bqq.results import Results
from bqq.service.info_service import InfoService
from bqq.service.result_service import ResultService
from bqq.types import JobInfo, SearchLine
from bqq.util import bash_util


def init():
    Path(const.BQQ_HOME).mkdir(exist_ok=True)
    Path(const.BQQ_RESULTS).mkdir(exist_ok=True)


@click.command()
@click.argument("sql", required=False)
@click.option("-f", "--file", help="File containing SQL", type=click.File("r"))
@click.option("-y", "--yes", help="Automatic yes to prompt", is_flag=True)
@click.option("-h", "--history", help="Search local history", is_flag=True)
@click.option("-d", "--delete", help="Delete job from history (local & cloud)", is_flag=True)
@click.option("-i", "--info", help="Show gcloud configuration", is_flag=True)
@click.option("--clear", help="Clear local history", is_flag=True)
@click.option("--sync", help="Sync history from cloud", is_flag=True)
@click.version_option()
def cli(
    sql: str, file: str, yes: bool, history: bool, delete: bool, clear: bool, sync: bool, info: bool
):
    """BiqQuery query."""
    init()
    job_info = None
    bq_client = BqClient()
    infos = Infos()
    results = Results()
    result_service = ResultService(bq_client, infos, results)
    info_service = InfoService(bq_client, result_service, infos)
    ctx = click.get_current_context()
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
        if infos:
            with bash_util.no_wrap():
                click.echo("\n".join([SearchLine.from_job_info(info).to_line for info in infos]))
            delete = click.confirm(f"Delete selected from history ({len(infos)})?", default=False)
            info_service.delete_infos(infos) if delete else click.echo(f"Nothing deleted.")
            ctx.exit()
    elif clear:
        size = len(infos.get_all())
        if click.confirm(f"Clear history ({size})?", default=False):
            infos.clear()
            results.clear()
            click.echo("All past results cleared")
        ctx.exit()
    elif sync:
        info_service.sync_infos()
    elif info:
        out = subprocess.check_output(["gcloud", "info", "--format=json"])
        gcloud_info = output.get_gcloud_info(json.loads(out))
        click.echo(gcloud_info)
        ctx.exit()
    else:
        click.echo(ctx.get_help())
        ctx.exit()
    if job_info:
        info_header = output.get_info_header(job_info)
        sql = output.get_sql(job_info)
        width = bash_util.get_max_width([info_header, sql])
        line = bash_util.hex_color(const.DARKER)("─" * width)
        lines = [line, info_header, line, sql, line]
        click.echo("\n".join(lines))
        result = results.read(job_info)
        if not result and click.confirm("Download result ?"):
            result_service.download_result(job_info.job_id)
            job_info = infos.find_by_id(job_info.job_id)  # updated job_info
            result = results.read(job_info)
        if result:
            if bash_util.use_less(result):
                os.environ["LESS"] += " -S"  # enable horizontal scrolling for less
                click.echo_via_pager(result)
            else:
                click.echo(result)
