from dataclasses import dataclass
from datetime import datetime
from dateutil.relativedelta import relativedelta


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

    @property
    def created_fmt(self) -> str:
        return self.created.strftime("%Y-%m-%d %H:%M:%S")

    @property
    def google_link(self) -> str:
        link = f"https://console.cloud.google.com/bigquery?project={self.project}&j=bq:{self.location}:{self.job_id}&page=queryresults"
        return link

    @property
    def slot_time(self) -> str:
        rd = relativedelta(microseconds=self.slot_millis * 1000)
        parts = [
            f" {rd.days}d" if rd.days else "",
            f" {rd.hours}h" if rd.hours else "",
            f" {rd.minutes}min" if rd.minutes else "",
            f" {rd.seconds}sec" if rd.seconds else "",
        ]
        return "".join(parts).strip()


@dataclass
class SearchResult:
    created: str
    query: str
    job_id: str
