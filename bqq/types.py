from dataclasses import dataclass
from datetime import datetime
from typing import Mapping, Optional
from dateutil.relativedelta import relativedelta
from google.cloud.bigquery.job.query import QueryJob

from bqq.util import bq_util


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
        )

    @property
    def created_fmt(self) -> str:
        return self.created.strftime("%Y-%m-%d %H:%M:%S")

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
        }


@dataclass
class SearchResult:
    created: str
    query: str
    job_id: str
