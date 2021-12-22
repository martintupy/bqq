from dataclasses import dataclass
from datetime import datetime
from typing import Mapping, Optional

from dateutil import tz
from dateutil.relativedelta import relativedelta
from google.cloud.bigquery.job.query import QueryJob
from tinydb.table import Document

from bqq import const
from bqq.util import bash_util, bq_util


@dataclass
class JobInfo:
    created: datetime
    query: str
    project: str
    location: str
    job_id: str
    bytes_billed: int
    cache_hit: bool
    slot_millis: int
    has_result: Optional[bool]
    account: str

    @staticmethod
    def from_query_job(job: QueryJob):
        return JobInfo(
            created=job.created,
            query=job.query,
            project=job.project,
            location=job.location,
            job_id=job.job_id,
            bytes_billed=job.total_bytes_billed,
            cache_hit=job.cache_hit,
            slot_millis=job.slot_millis,
            has_result=None,
            account=job.user_email,
        )

    @staticmethod
    def from_document(doc: Document):
        return JobInfo(
            created=datetime.fromisoformat(doc["created"]),
            query=doc.get("query"),
            project=doc.get("project"),
            location=doc.get("location"),
            job_id=doc.get("job_id"),
            bytes_billed=doc.get("bytes_billed"),
            cache_hit=doc.get("cache_hit"),
            slot_millis=doc.get("slot_millis"),
            has_result=doc.get("has_result"),
            account=doc.get("account"),
        )

    @property
    def created_fmt(self) -> str:
        return self.created.astimezone(tz.tzlocal()).strftime("%Y-%m-%d %H:%M:%S")

    @property
    def google_link(self) -> str:
        link = f"https://console.cloud.google.com/bigquery?project={self.project}&j=bq:{self.location}:{self.job_id}&page=queryresults"
        return link

    @property
    def price_fmt(self) -> str:
        bytes = self.bytes_billed or 0
        return bq_util.price_fmt(bytes)

    @property
    def slot_time(self) -> str:
        millis = self.slot_millis or 0
        rd = relativedelta(microseconds=millis * 1000)
        parts = [
            f" {rd.days}d" if rd.days else "",
            f" {rd.hours}h" if rd.hours else "",
            f" {rd.minutes}min" if rd.minutes else "",
            f" {rd.seconds}sec" if rd.seconds else "",
        ]
        return "".join(parts).strip()

    @property
    def mapping(self) -> Mapping:
        return {
            "created": self.created.isoformat(),
            "query": self.query,
            "project": self.project,
            "location": self.location,
            "job_id": self.job_id,
            "bytes_billed": self.bytes_billed,
            "cache_hit": self.cache_hit,
            "slot_millis": self.slot_millis,
            "has_result": self.has_result,
            "account": self.account,
        }


@dataclass
class SearchLine:
    created: str
    query: str
    job_id: str

    @staticmethod
    def from_line(line: str):
        parts = line.split(const.FZF_SEPARATOR)
        search_result = None
        if len(parts) == 3:
            search_result = SearchLine(
                created=parts[0],
                query=parts[1],
                job_id=parts[2],
            )
        return search_result

    @staticmethod
    def from_job_info(job_info: JobInfo):
        return SearchLine(
            created=bash_util.hex_color(const.TIME)(job_info.created_fmt),
            query=bash_util.color_keywords(" ".join(job_info.query.split())),
            job_id=bash_util.hex_color(const.ID)(job_info.job_id),
        )

    @property
    def to_line(self):
        return const.FZF_SEPARATOR.join([self.created, self.query, self.job_id])
