from pathlib import Path
import os
import yaml
from rich.style import Style
from rich.theme import Theme

BQQ_HOME = os.environ.get("BQQ_HOME", f"{Path.home()}/.bqq")
BQQ_RESULTS = os.environ.get("BQQ_RESULTS", f"{BQQ_HOME}/results")

BQQ_MAX_LINES = os.environ.get("BQQ_MAX_LINES", 400)
BQQ_MAX_RESULT_ROWS = os.environ.get("BQQ_MAX_RESULT_ROWS", 1_000)

BQQ_DISABLE_COLORS = os.getenv("BQQ_DISABLE_COLORS", "False").lower() in ("true", "1", "t")
default_skin = os.path.join(os.path.dirname(__file__), "default-skin.yaml")
BQQ_SKIN = os.environ.get("BQQ_SKIN", default_skin)

skin: dict = yaml.safe_load(open(BQQ_SKIN, "r"))
ERROR = skin.get("bqq", {}).get("error")
DARKER = skin.get("bqq", {}).get("darker")
INFO = skin.get("bqq", {}).get("info")
LINK = skin.get("bqq", {}).get("link")
KEYWORD = skin.get("bqq", {}).get("keyword")
ID = skin.get("bqq", {}).get("id")
TIME = skin.get("bqq", {}).get("time")

error_style = Style(color=ERROR)
darker_style = Style(color=DARKER)
info_style = Style(color=INFO)
link_style = Style(color=LINK)
keyword_style = Style(color=KEYWORD)
id_style = Style(color=ID)
time_style = Style(color=TIME)

theme = Theme(
    {
        "progress.elapsed": "dim",
        "prompt.default": "dim",
        "prompt.choices": "none",
        "rule.line": "dim",
    }
)

FZF_SEPARATOR = " ~ "

HISTORY_DAYS = 30

BQ_KEYWORDS = [
    "ALL",
    "AND",
    "ANY",
    "ARRAY",
    "AS",
    "ASC",
    "ASSERT_ROWS_MODIFIED",
    "AT",
    "BETWEEN",
    "BY",
    "CASE",
    "CAST",
    "COLLATE",
    "CONTAINS",
    "CREATE",
    "CROSS",
    "CUBE",
    "CURRENT",
    "DEFAULT",
    "DEFINE",
    "DESC",
    "DISTINCT",
    "ELSE",
    "END",
    "ENUM",
    "ESCAPE",
    "EXCEPT",
    "EXCLUDE",
    "EXISTS",
    "EXTRACT",
    "FALSE",
    "FETCH",
    "FOLLOWING",
    "FOR",
    "FROM",
    "FULL",
    "GROUP",
    "GROUPING",
    "GROUPS",
    "HASH",
    "HAVING",
    "IF",
    "IGNORE",
    "IN",
    "INNER",
    "INTERSECT",
    "INTERVAL",
    "INTO",
    "IS",
    "JOIN",
    "LATERAL",
    "LEFT",
    "LIKE",
    "LIMIT",
    "LOOKUP",
    "MERGE",
    "NATURAL",
    "NEW",
    "NO",
    "NOT",
    "NULL",
    "NULLS",
    "OF",
    "ON",
    "OR",
    "ORDER",
    "OUTER",
    "OVER",
    "PARTITION",
    "PRECEDING",
    "PROTO",
    "RANGE",
    "RECURSIVE",
    "RESPECT",
    "RIGHT",
    "ROLLUP",
    "ROWS",
    "SELECT",
    "SET",
    "SOME",
    "STRUCT",
    "TABLESAMPLE",
    "THEN",
    "TO",
    "TREAT",
    "TRUE",
    "UNBOUNDED",
    "UNION",
    "UNNEST",
    "USING",
    "WHEN",
    "WHERE",
    "WINDOW",
    "WITH",
    "WITHIN",
]
