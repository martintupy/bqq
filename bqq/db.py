from typing import Optional

from tinydb import Query, TinyDB
from tinydb.table import Document

from bqq import util
from bqq.const import BQQ_HOME

db = TinyDB(f"{BQQ_HOME}/db.json")
Q = Query()


def clear():
    db.clear_cache()
    db.truncate()


def pick_query() -> str:
    queries = reversed([row["query"] for row in db.all()])
    query = util.fzf(queries)
    if query:
        return db.search(Q.query == query)[0]["date"]
    else:
        return None


def pick_date() -> str:
    dates = reversed([row["date"] for row in db.all()])
    date = util.fzf(dates)
    return date


def find_date(date: str) -> Optional[Document]:
    try:
        return db.search(Q.date == date)[0]
    except IndexError:
        None


def insert_query(date: str, query: str, job_id: str):
    min_query = " ".join(query.split())
    db.insert({"date": date, "query": min_query, "job_id": job_id})
