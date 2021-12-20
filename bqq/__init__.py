import os
from typing import Optional, Tuple

import click
from google.cloud.bigquery import Client


from bqq import db, result
from bqq.bq_util import dry_run, get_header, run_query
from bqq.data import Metadata
from bqq.util import result_header, use_less, color_keywords


@click.command()
@click.argument("sql", required=False)
@click.option("-f", "--file", help="File containing SQL", type=click.File("r"))
@click.option("-y", "--yes", help="Automatic yes to prompt", is_flag=True)
@click.option("-r", "--results", help="Search past results", is_flag=True)
@click.option("--clear", help="Clear all past results", is_flag=True)
def cli(sql: str, file: str, yes: bool, results: bool, clear: bool):
    """BiqQuery query."""
    metadata = None
    if file:
        query = file.read()
        metadata = call_api(yes, query)
    elif sql:
        query = sql
        metadata = call_api(yes, query)
    elif results:
        metadata = db.results()
    elif clear:
        ctx = click.get_current_context()
        if click.confirm("Clear all results?", default=False):
            db.clear()
            result.clear()
            click.echo("All past results cleared")
        ctx.exit()
    else:
        ctx = click.get_current_context()
        click.echo(ctx.get_help())
        ctx.exit()

    if metadata:
        message = f"{result_header(metadata)}\n"
        message += result.read(metadata.job_id).get_string()
        if use_less(message):
            os.environ["LESS"] += " -S"  # enable horizontal scrolling for less
            click.echo_via_pager(message)
        else:
            click.echo(message)


def call_api(yes: bool, query: str) -> Optional[Metadata]:
    client = Client()
    job = dry_run(client, query)
    confirmed = yes
    metadata = None
    if not confirmed and job:
        click.echo(get_header(job, client.project))
        confirmed = click.confirm("Do you want to continue?", default=False)
    if confirmed and job:
        date, job_id = run_query(client, query)
        metadata = Metadata(date, query, job_id)
    return metadata
