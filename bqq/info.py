from datetime import datetime
from typing import List, Optional

import sqlparse
from tinydb import Query, TinyDB

from bqq import const
from bqq.types import JobInfo

db = TinyDB(f"{const.BQQ_HOME}/db.json")
Q = Query()


def clear():
    db.clear_cache()
    db.truncate()


def find_date(date: str) -> Optional[JobInfo]:
    job_info = None
    try:
        job_info = db.search(Q.date == date)[0]
    except IndexError:
        job_info = None
    return job_info


def get_all() -> List[JobInfo]:
    all = []
    for row in db.all():
        all.append(
            JobInfo(
                created=datetime.fromisoformat(row["created"]),
                query=row["query"],
                project=row["project"],
                location=row["location"],
                job_id=row["job_id"],
            )
        )
    return all


def insert(info: JobInfo):
    query = sqlparse.format(info.query, strip_comments=True)
    min_query = " ".join(query.split())
    db.insert(
        {
            "created": info.created.isoformat(),
            "query": min_query,
            "project": info.project,
            "location": info.location,
            "job_id": info.job_id,
        }
    )
