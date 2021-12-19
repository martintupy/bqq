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
@click.option("--dates", help="Search results from past execution dates", is_flag=True)
@click.option("--queries", help="Search results from past queries", is_flag=True)
@click.option("--clear", help="Clear all past results", is_flag=True)
def cli(sql: str, file: str, dates: bool, queries: bool, yes: bool, clear: bool):
    """BiqQuery query."""
    date = None
    if file:
        query = file.read()
        date = call_api(yes, query)
    elif sql:
        query = sql
        date = call_api(yes, query)
    elif dates:
        date = db.pick_date()
    elif queries:
        date = db.pick_query()
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

    if date:
        message = result.read(date).get_string()
        if use_less(message):
            os.environ["LESS"] += " -S"  # enable horizontal scrolling for less
            click.echo_via_pager(message)
        else:
            click.echo(message)


def call_api(yes: bool, query: str):
    client = Client()
    job = dry_run(client, query)
    confirmed = yes
    date = None
    if not confirmed and job:
        click.echo(get_header(job, client.project))
        confirmed = click.confirm("Do you want to continue?", default=False)
    if confirmed and job:
        date = run_query(client, query)
    return date
