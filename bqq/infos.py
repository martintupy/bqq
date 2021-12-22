from datetime import datetime
from typing import List, Optional

from tinydb import Query, TinyDB

from bqq import const
from bqq.types import JobInfo


class Infos:
    def __init__(self) -> None:
        self.InfoQuery = Query()
        self.db = TinyDB(f"{const.BQQ_HOME}/db.json")

    def clear(self):
        self.db.clear_cache()
        self.db.truncate()

    def find_date(self, date: str) -> Optional[JobInfo]:
        job_info = None
        try:
            job_info = self.db.search(self.InfoQuery.date == date)[0]
        except IndexError:
            job_info = None
        return job_info

    def get_all(self) -> List[JobInfo]:
        all = []
        for row in self.db.all():
            all.append(
                JobInfo(
                    created=datetime.fromisoformat(row["created"]),
                    query=row.get("query"),
                    project=row.get("project"),
                    location=row.get("location"),
                    job_id=row.get("job_id"),
                    bytes_billed=row.get("bytes_billed"),
                    cache_hit=row.get("cache_hit"),
                    slot_millis=row.get("slot_millis"),
                )
            )
        return all

    def insert(self, info: JobInfo):
        self.db.insert(info.mapping)

    def upsert(self, info: JobInfo):
        self.db.upsert(info.mapping, self.InfoQuery.job_id == info.job_id)

    def remove(self, info: JobInfo):
        self.db.remove(self.InfoQuery.job_id == info.job_id)
