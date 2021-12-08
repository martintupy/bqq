import click
from google.cloud import bigquery

from bqq.bq_util import estimate_size, run_query


@click.command()
@click.argument("sql", required=False)
@click.option("-f", "--file", help="File containing SQL", type=click.File("r"))
def cli(sql, file):
    """BiqQuery query."""
    if file:
        query = file.read()
    else:
        query = sql

    client = bigquery.Client()
    size = estimate_size(client, query)
    click.echo(f"Estimated size: {size}")
    if click.confirm("Do you want to continue?", default=False):
        table = run_query(client, query)
        click.echo(table.get_string())
        
