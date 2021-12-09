from typing import Optional
from uuid import UUID

from tinydb import Query, TinyDB
from tinydb.table import Document

from bqq.const import BQQ_HOME

db = TinyDB(f"{BQQ_HOME}/db.json")
Q = Query()


def find_id(query: str) -> Optional[UUID]:
    min_query = " ".join(query.split())
    try:
        result = db.search(Q.query == min_query)[0]
        return UUID(result.get("id"))
    except IndexError:
        pass


def insert_id(query: str, id: UUID):
    min_query = " ".join(query.split())
    db.insert({"query": min_query, "id": str(id)})
