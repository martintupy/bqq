import os

import click
from google.cloud.bigquery import Client

from bqq import db, result
from bqq.bq_util import dry_run, get_header, run_query
from bqq.util import use_less


@click.command()
@click.argument("sql", required=False)
@click.option("-f", "--file", help="File containing SQL", type=click.File("r"))
@click.option("-y", "--yes", help="Automatic yes to prompt", is_flag=True)
@click.option("-r", "--results", help="Search past results", is_flag=True)
@click.option("--clear", help="Clear all past results", is_flag=True)
def cli(sql: str, file: str, yes: bool, results: bool, clear: bool):
    """BiqQuery query."""
    job_id = None
    if file:
        query = file.read()
        job_id = call_api(yes, query)
    elif sql:
        query = sql
        job_id = call_api(yes, query)
    elif results:
        job_id = db.results()
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

    if job_id:
        message = result.read(job_id).get_string()
        if use_less(message):
            os.environ["LESS"] += " -S"  # enable horizontal scrolling for less
            click.echo_via_pager(message)
        else:
            click.echo(message)


def call_api(yes: bool, query: str):
    client = Client()
    job = dry_run(client, query)
    confirmed = yes
    job_id = None
    if not confirmed and job:
        click.echo(get_header(job, client.project))
        confirmed = click.confirm("Do you want to continue?", default=False)
    if confirmed and job:
        job_id = run_query(client, query)
    return job_id
