from google.api_core.page_iterator import Page
from google.cloud.bigquery import Client, QueryJobConfig
from prettytable import PrettyTable
from prettytable.prettytable import PLAIN_COLUMNS

from bqq.util import num_fmt, hex


def estimate_size(client: Client, query: str):
    job_config = QueryJobConfig()
    job_config.dry_run = True
    job = client.query(query, job_config=job_config)
    return num_fmt(job.total_bytes_processed)


def run_query(client: Client, query: str) -> PrettyTable:
    result = client.query(query).result()
    table = PrettyTable()
    table.field_names = [hex("58A33B")(field.name) for field in result.schema]
    for row in result:
        table.add_row(row)
    table.align = "l"
    table.vertical_char = hex("545454")("|")
    table.horizontal_char = hex("545454")("-")
    table.junction_char = hex("545454")("+")
    return table
