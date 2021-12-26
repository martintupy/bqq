from datetime import datetime, timedelta
from typing import List, Optional

import click
from bqq import const
from bqq.bq_client import BqClient
from bqq.infos import Infos
from bqq.results import Results
from google.api_core.exceptions import BadRequest, NotFound
from google.cloud.bigquery.job.query import QueryJob


class ResultService:
    def __init__(self, bq_client: BqClient, infos: Infos, results: Results):
        self.bq_client = bq_client
        self.infos = infos
        self.results = results

    def write_result(self, query_job: QueryJob):
        try:
            rows = query_job.result(max_results=const.BQQ_MAX_RESULT_ROWS)
            self.results.write(query_job.project, query_job.job_id, rows)
        except (BadRequest, NotFound) as e:
            self.infos.update_has_result(query_job.job_id, False)

    def download_result(self, job_id: str):
        job = self.bq_client.client.get_job(job_id)
        if isinstance(job, QueryJob):
            self.write_result(job)
        else:
            click.echo("Query job doesn't exist")
