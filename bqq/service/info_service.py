from datetime import datetime
from google.cloud.bigquery.job.query import QueryJob

import sqlparse
from bqq import const, info
from bqq.types import JobInfo, SearchResult
from bqq.util import bash_util


def search() -> JobInfo:
    sep = " ~ "
    results = []
    job_info = None
    rows = info.get_all()
    for row in rows:
        date = bash_util.hex_color(const.HIGHTLIGHT)(row.created_fmt)
        query = bash_util.color_keywords(row.query)
        job_id = bash_util.hex_color(const.ID)(row.job_id)
        result = sep.join([date, query, job_id])
        results.append(result)
    pick = bash_util.fzf(reversed(results))
    result = pick.split(sep)
    if len(result) == 3:
        job_id = result[2]
        job_info = next((row for row in rows if row.job_id == job_id), None)
    return job_info


def get_header(job_info: JobInfo) -> str:
    sql = sqlparse.format(job_info.query, reindent=True)
    width, _ = bash_util.get_size(sql)
    return (
        bash_util.hex_color(const.HEADER)("Creation time")
        + f" = {bash_util.hex_color(const.HIGHTLIGHT)(job_info.created_fmt)}\n"
        + bash_util.hex_color(const.HEADER)("Console link")
        + f" = {bash_util.hex_color(const.LINK)(job_info.google_link)}\n"
        + f"{bash_util.hex_color(const.DARKER)('-' * width)}\n"
        + bash_util.color_keywords(sql)
    )
