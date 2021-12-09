from google.api_core.page_iterator import Page
from google.cloud.bigquery import Client, QueryJobConfig
from prettytable import PrettyTable

from bqq.util import num_fmt


def estimate_size(client: Client, query: str):
    job_config = QueryJobConfig()
    job_config.dry_run = True
    job = client.query(query, job_config=job_config)
    return num_fmt(job.total_bytes_processed)


def run_query(client: Client, query: str) -> PrettyTable:
    result = client.query(query).result()
    table = PrettyTable()
    table.field_names = [field.name for field in result.schema]
    for row in result:
        table.add_row(row)
    return table
