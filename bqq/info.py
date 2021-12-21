from datetime import datetime
from typing import List, Optional

import sqlparse
from tinydb import Query, TinyDB

from bqq import const
from bqq.types import JobInfo

db = TinyDB(f"{const.BQQ_HOME}/db.json")
JobInfoQuery = Query()


def clear():
    db.clear_cache()
    db.truncate()


def find_date(date: str) -> Optional[JobInfo]:
    job_info = None
    try:
        job_info = db.search(JobInfoQuery.date == date)[0]
    except IndexError:
        job_info = None
    return job_info


def get_all() -> List[JobInfo]:
    all = []
    for row in db.all():
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


def insert(info: JobInfo):
    db.insert(info.mapping)


def upsert(info: JobInfo):
    db.upsert(info.mapping, JobInfoQuery.job_id == info.job_id)
