from dataclasses import dataclass
from datetime import datetime


@dataclass
class JobInfo:
    created: datetime
    query: str
    project: str
    location: str
    job_id: str

    @property
    def created_fmt(self) -> str:
        return self.created.strftime("%Y-%m-%d %H:%M:%S")

    @property
    def google_link(self) -> str:
        link = f"https://console.cloud.google.com/bigquery?project={self.project}&j=bq:{self.location}:{self.job_id}&page=queryresults"
        return link


@dataclass
class SearchResult:
    created: str
    query: str
    job_id: str
