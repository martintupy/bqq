from datetime import datetime
from typing import Optional

from tinydb import Query, TinyDB
from tinydb.table import Document

from bqq import util
from bqq.const import BQQ_HOME, HIGHTLIGHT, ID

db = TinyDB(f"{BQQ_HOME}/db.json")
Q = Query()


def clear():
    db.clear_cache()
    db.truncate()


def results() -> str:
    sep = " - "
    results = []
    for row in db.all():
        datefmt = datetime.fromisoformat(row["date"]).strftime("%Y-%m-%d %H:%M:%S")
        date = util.hex_color(HIGHTLIGHT)(datefmt)
        query = util.color_keywords(row["query"])
        job_id = util.hex_color(ID)(row["job_id"])
        result = sep.join([date, query, job_id])
        results.append(result)
    pick = util.fzf(reversed(results))
    job_id = pick.split(sep)[-1]
    return job_id


def find_date(date: str) -> Optional[Document]:
    try:
        return db.search(Q.date == date)[0]
    except IndexError:
        None


def insert_query(date: str, query: str, job_id: str):
    min_query = " ".join(query.split())
    db.insert({"date": date, "query": min_query, "job_id": job_id})
