import json
import os
import subprocess
from pathlib import Path
from rich.console import Console

import click
from rich.text import Text

from bqq import const, output
from bqq.bq_client import BqClient
from bqq.infos import Infos
from bqq.results import Results
from bqq.service.info_service import InfoService
from bqq.service.result_service import ResultService
from rich.prompt import Confirm


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
def cli(sql: str, file: str, yes: bool, history: bool, delete: bool, clear: bool, sync: bool, info: bool):
    """BiqQuery query."""
    init()
    job_info = None
    console = Console(theme=const.theme)
    bq_client = BqClient(console)
    infos = Infos()
    results = Results(console)
    result_service = ResultService(console, bq_client, infos, results)
    info_service = InfoService(console, bq_client, result_service, infos)
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
            if Confirm.ask(f"Delete selected ({len(infos)})?", default=True, console=console):
                info_service.delete_infos(infos)
            else:
                console.print(f"Nothing deleted.")
            ctx.exit()
    elif clear:
        size = len(infos.get_all())
        if Confirm.ask(f"Clear all ({size})?", default=False, console=console):
            infos.clear()
            results.clear()
            console.print("All cleared.")
        ctx.exit()
    elif sync:
        info_service.sync_infos()
    elif info:
        out = subprocess.check_output(["gcloud", "info", "--format=json"])
        gcloud_info = output.get_gcloud_info(json.loads(out))
        console.print(gcloud_info)
        ctx.exit()
    else:
        console.print(ctx.get_help())
        ctx.exit()

    # ---------------------- output -------------------------
    if job_info:
        header = output.get_info_header(job_info)
        console.rule()
        console.print(header)
        console.rule()
        sql = output.get_sql(job_info)
        console.print(sql)
        console.rule()
        result = results.read(job_info)
        if not result and job_info.has_result is None:
            if Confirm.ask("Download result?", default=False, console=console):
                result_service.download_result(job_info.job_id)
                job_info = infos.find_by_id(job_info.job_id)  # updated job_info
                result = results.read(job_info)
        if job_info.has_result is False:
            console.print("Query result has expired", style=const.error_style)
            console.rule()
            if Confirm.ask("Re-execute query?", default=False, console=console):
                job_info = info_service.get_info(True, job_info.query)
                result = results.read(job_info)
        if result:
            if result.width > console.width:
                with console.pager(styles=True):
                    os.environ["LESS"] += " -S"  # enable horizontal scrolling for less
                    console.print(result, crop=False)
            else:
                console.print(result, crop=False)
