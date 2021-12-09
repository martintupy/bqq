import os

import click
from google.cloud.bigquery import Client

from bqq.bq_util import estimate, run_query
from bqq.csv import read_csv
from bqq.db import find_id


@click.command()
@click.argument("sql", required=False)
@click.option("-f", "--file", help="File containing SQL", type=click.File("r"))
@click.option("-y", "--yes", help="Automatic yes to prompt", is_flag=True)
def cli(sql, file, yes):
    """BiqQuery query."""
    if file:
        query = file.read()
    else:
        query = sql

    id = find_id(query)
    if id:
        click.echo(f"Using cached query")
    else:
        client = Client()
        size, cost = estimate(client, query)
        confirmed = yes
        if not confirmed:
            click.echo(f"Estimated size: {size} cost: {cost}")
            confirmed = click.confirm("Do you want to continue?", default=False)
        if confirmed:
            id = run_query(client, query)

    if id:
        message = read_csv(id).get_string()
        os.environ["LESS"] += " -S"  # enable horizontal scrolling for less
        click.echo_via_pager(message)
