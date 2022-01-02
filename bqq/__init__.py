import json
import os
import subprocess
from pathlib import Path

import click
from rich.console import Console, Group, NewLine
from rich.prompt import Confirm, Prompt
from rich.text import Text
from rich.panel import Panel

from bqq import const, output
from bqq.bq_client import BqClient
from bqq.data.infos import Infos
from bqq.data.results import Results
from bqq.data.schemas import Schemas
from bqq.service.info_service import InfoService
from bqq.service.result_service import ResultService


@click.command()
@click.argument("sql", required=False)
@click.option("-f", "--file", help="File containing SQL", type=click.File("r"))
@click.option("-y", "--yes", help="Automatic yes to prompt", is_flag=True)
@click.option("-h", "--history", help="Search local history", is_flag=True)
@click.option("-d", "--delete", help="Delete job from history (local & cloud)", is_flag=True)
@click.option("-i", "--info", help="Show gcloud configuration", is_flag=True)
@click.option("--clear", help="Clear local history", is_flag=True)
@click.option("--sync", help="Sync history from cloud", is_flag=True)
@click.option("--init", help="Initialize bqq environment", is_flag=True)
@click.version_option()
def cli(sql: str, file: str, yes: bool, history: bool, delete: bool, clear: bool, sync: bool, init: bool, info: bool):
    """BiqQuery query."""
    console = Console(theme=const.theme)
    bq_client = BqClient(console)
    infos = Infos()
    results = Results(console)
    schemas = Schemas()
    result_service = ResultService(console, bq_client, infos, results, schemas)
    info_service = InfoService(console, bq_client, result_service, infos)
    ctx = click.get_current_context()
    job_info = None
    if init:
        initialize(console)
        ctx.exit()
    elif not os.path.exists(const.BQQ_HOME):
        console.print(
            Panel(
                title="Not initialized, run",
                renderable=Text("bqq --init"),
                expand=False,
                padding=(1, 3),
                border_style=const.warning_style,
            )
        )
        ctx.exit()
    elif file:
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
            schemas.clear()
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
        result_table = result_service.get_table(job_info)
        if not result_table and job_info.has_result is None:
            if Confirm.ask("Download result?", default=False, console=console):
                result_service.download_result(job_info.job_id)
                job_info = infos.find_by_id(job_info.job_id)  # updated job_info
                result_table = result_service.get_table(job_info)
        if job_info.has_result is False:
            console.print("Query result has expired", style=const.error_style)
            console.rule()
            if Confirm.ask("Re-execute query?", default=False, console=console):
                job_info = info_service.get_info(True, job_info.query)
                result_table = result_service.get_table(job_info)
        if result_table:
            if result_table.width > console.width:
                with console.pager(styles=True):
                    os.environ["LESS"] += " -S"  # enable horizontal scrolling for less
                    console.print(result_table, crop=False)
            else:
                console.print(result_table, crop=False)


def initialize(console: Console):
    bqq_home = Prompt.ask("Enter bqq home path", default=const.DEFAULT_BQQ_HOME, console=console)
    bqq_results = f"{bqq_home}/results"
    bqq_schemas = f"{bqq_home}/schemas"
    bqq_infos = f"{bqq_home}/infos.json"
    bqq_config = f"{bqq_home}/config.yaml"

    Path(bqq_home).mkdir(parents=True, exist_ok=True)
    console.print(f"created - {bqq_home}")
    Path(bqq_results).mkdir(parents=True, exist_ok=True)
    console.print(f"created - {bqq_results}")
    Path(bqq_schemas).mkdir(parents=True, exist_ok=True)
    console.print(f"created - {bqq_schemas}")
    Path(bqq_infos).touch()
    console.print(f"created - {bqq_infos}")
    Path(bqq_config).touch()
    console.print(f"created - {bqq_config}")

    if bqq_home != const.DEFAULT_BQQ_HOME:
        group = Group(Text(f"export BQQ_HOME={bqq_home}"))
        console.print(
            NewLine(),
            Panel(
                title="Export following to your environment",
                renderable=group,
                expand=False,
                padding=(1, 3),
                border_style=const.warning_style,
            ),
        )
