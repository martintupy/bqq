import uuid
from uuid import UUID

from google.cloud.bigquery import Client, QueryJobConfig

from bqq.csv import write_csv
from bqq.db import insert_id
from bqq.util import price_fmt, size_fmt


def estimate(client: Client, query: str):
    job_config = QueryJobConfig()
    job_config.dry_run = True
    job = client.query(query, job_config=job_config)
    size = size_fmt(job.total_bytes_processed)
    cost = price_fmt(job.total_bytes_processed)
    return size, cost


def run_query(client: Client, query: str) -> UUID:
    id = uuid.uuid4()
    result = client.query(query).result()
    header = [field.name for field in result.schema]
    rows = list(result)
    insert_id(query, id)
    write_csv(id, header, rows)
    return id
