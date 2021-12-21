from datetime import datetime

import sqlparse
from bqq import const, info
from bqq.types import JobInfo
from bqq.util import bash_util, bq_util
from tinydb.queries import Query


def search() -> JobInfo:
    results = []
    job_info = None
    rows = info.get_all()
    for row in rows:
        created = bash_util.hex_color(const.TIME)(row.created_fmt)
        query_min = " ".join(row.query.split())
        query = bash_util.color_keywords(query_min)
        job_id = bash_util.hex_color(const.ID)(row.job_id)
        result = const.FZF_SEPARATOR.join([created, query, job_id])
        results.append(result)
    pick = bash_util.fzf(results)
    result = pick.split(const.FZF_SEPARATOR)
    if len(result) == 3:
        job_id = result[2]
        job_info = next((row for row in rows if row.job_id == job_id), None)
    return job_info


def get_info(job_info: JobInfo) -> str:
    cache_hit = "(cache hit)" if job_info.cache_hit else ""
    console_link = bash_util.hex_color(const.LINK)(job_info.google_link)
    lines = [
        f"{bash_util.hex_color(const.INFO)('Creation time')} = {job_info.created_fmt}",
        f"{bash_util.hex_color(const.INFO)('Query cost')} = {job_info.price_fmt} {cache_hit}",
        f"{bash_util.hex_color(const.INFO)('Slot time')} = {job_info.slot_time}",
        f"{bash_util.hex_color(const.INFO)('Console link')} = {console_link}",
    ]
    info = "\n".join(lines)
    width, _ = bash_util.get_size(info)
    result_lines = [
        f"{bash_util.hex_color(const.DARKER)('─' * width)}",
        info,
        f"{bash_util.hex_color(const.DARKER)('─' * width)}",
    ]
    return "\n".join(result_lines)


def get_sql(job_info: JobInfo) -> str:
    sql = sqlparse.format(job_info.query, reindent=True)
    return bash_util.color_keywords(sql)
