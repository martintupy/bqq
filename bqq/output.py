from google.cloud.bigquery.job.query import QueryJob

from bqq import const
from bqq.types import JobInfo
from bqq.util import bash_util, bq_util


def get_dry_info_header(job: QueryJob) -> str:
    size = bq_util.size_fmt(job.total_bytes_processed)
    cost = bq_util.price_fmt(job.total_bytes_processed)
    lines = [
        f"{bash_util.hex_color(const.INFO)('Billing project')} = {job.project}",
        f"{bash_util.hex_color(const.INFO)('Estimated size')} = {size}",
        f"{bash_util.hex_color(const.INFO)('Estimated cost')} = {cost}",
    ]
    return "\n".join(lines)


def get_info_header(job_info: JobInfo) -> str:
    cache_hit = "(cache hit)" if job_info.cache_hit else ""
    console_link = bash_util.hex_color(const.LINK)(job_info.google_link)
    lines = [
        f"{bash_util.hex_color(const.INFO)('Creation time')} = {job_info.created_fmt}",
        f"{bash_util.hex_color(const.INFO)('Project')} = {job_info.project}",
        f"{bash_util.hex_color(const.INFO)('Account')} = {job_info.account}",
        f"{bash_util.hex_color(const.INFO)('Query cost')} = {job_info.price_fmt} {cache_hit}",
        f"{bash_util.hex_color(const.INFO)('Slot time')} = {job_info.slot_time}",
        f"{bash_util.hex_color(const.INFO)('Console link')} = {console_link}",
    ]
    return "\n".join(lines)


def get_sql(job_info: JobInfo) -> str:
    return bash_util.color_keywords(job_info.query)


def get_gcloud_info(json: dict) -> str:
    project = json.get("config", {}).get("project")
    account = json.get("config", {}).get("account")
    lines = [
        f"{bash_util.hex_color(const.INFO)('Project')} = {project}",
        f"{bash_util.hex_color(const.INFO)('Account')} = {account}",
    ]
    return "\n".join(lines)
