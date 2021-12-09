import click
from google.cloud import bigquery
from prettytable import PrettyTable

from bqq.bq_util import estimate_size, run_query


@click.command()
@click.argument("sql", required=False)
@click.option("-f", "--file", help="File containing SQL", type=click.File("r"))
@click.option("-y", "--yes", help="Automatic yes to prompt", is_flag=True)
@click.option("--pager", help="Output via pager", is_flag=True)
def cli(sql, file, yes, pager):
    """BiqQuery query."""
    if file:
        query = file.read()
    else:
        query = sql

    client = bigquery.Client()
    size = estimate_size(client, query)
    
    confirmed = yes
    if not confirmed:
        click.echo(f"Estimated size: {size}")
        confirmed = click.confirm("Do you want to continue?", default=False)

    if confirmed:
        message = run_query(client, query).get_string()
        if pager:
            click.echo_via_pager(message)
        else:
            click.echo(message)
