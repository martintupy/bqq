from datetime import datetime

import click
from google.api_core.exceptions import BadRequest
from google.cloud.bigquery import Client, QueryJobConfig
from prettytable import PrettyTable

from bqq import util
from bqq.const import ERROR, HIGHTLIGHT, TABLE_BORDER, TABLE_HEADER
from bqq.db import insert_query
from bqq.result import write
from bqq.util import price_fmt, size_fmt


def dry_run(client: Client, query: str):
    job_config = QueryJobConfig()
    job_config.dry_run = True
    job = None
    try:
        job = client.query(query, job_config=job_config)
    except BadRequest as e:
        click.echo(util.hex_color(ERROR)(e.message), err=True)
    return job


def run_query(client: Client, query: str) -> str:
    q = client.query(query)
    job_id = q.job_id
    result = q.result()
    date = datetime.utcnow().isoformat()
    header = [field.name for field in result.schema]
    rows = list(result)
    insert_query(date, query, job_id)
    write(job_id, header, rows)
    return job_id


def get_header(job, project) -> str:
    size = size_fmt(job.total_bytes_processed)
    cost = price_fmt(job.total_bytes_processed)
    table = PrettyTable()
    table.vertical_char = util.hex_color(TABLE_BORDER)("|")
    table.horizontal_char = util.hex_color(TABLE_BORDER)("-")
    table.junction_char = util.hex_color(TABLE_BORDER)("+")
    table.field_names = [
        util.hex_color(TABLE_HEADER)("Billed project"),
        util.hex_color(TABLE_HEADER)("Estimated cost"),
        util.hex_color(TABLE_HEADER)("Estimated size"),
    ]
    table.add_row(
        [
            util.hex_color(HIGHTLIGHT)(project),
            util.hex_color(HIGHTLIGHT)(cost),
            util.hex_color(HIGHTLIGHT)(size),
        ]
    )
    return table.get_string()
