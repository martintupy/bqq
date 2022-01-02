from pathlib import Path
import os
import yaml
from rich.style import Style
from rich.theme import Theme

DEFAULT_BQQ_HOME = f"{Path.home()}/.bqq"

BQQ_HOME = os.getenv("BQQ_HOME", DEFAULT_BQQ_HOME)
BQQ_RESULTS = f"{BQQ_HOME}/results"
BQQ_SCHEMAS = f"{BQQ_HOME}/schemas"
BQQ_INFOS = f"{BQQ_HOME}/infos.json"
BQQ_CONFIG = f"{BQQ_HOME}/config.yaml"

BQQ_MAX_RESULT_ROWS = os.getenv("BQQ_MAX_RESULT_ROWS", 1_000)

BQQ_DISABLE_COLORS = os.getenv("BQQ_DISABLE_COLORS", "False").lower() in ("true", "1", "t")
BQQ_SKIN = os.getenv("BQQ_SKIN")

default_skin = {
    "error": "red",
    "warning": "gold3",
    "border": "grey27",
    "darker": "grey46",
    "info": "green",
    "link": "light_sky_blue1",
    "keyword": "dodger_blue1",
}

skin = default_skin

if BQQ_SKIN and os.path.isfile(BQQ_SKIN):
    skin = yaml.safe_load(open(BQQ_SKIN, "r"))

ERROR = skin.get("error", default_skin["error"])
WARNING = skin.get("warning", default_skin["warning"])
BORDER = skin.get("border", default_skin["border"])
DARKER = skin.get("darker", default_skin["darker"])
INFO = skin.get("info", default_skin["info"])
LINK = skin.get("link", default_skin["link"])
KEYWORD = skin.get("keyword", default_skin["keyword"])

error_style = Style(color=ERROR)
warning_style = Style(color=WARNING)
border_style = Style(color=BORDER)
darker_style = Style(color=DARKER)
info_style = Style(color=INFO)
link_style = Style(color=LINK)
keyword_style = Style(color=KEYWORD)

theme = Theme(
    {
        "progress.elapsed": darker_style,
        "prompt.default": darker_style,
        "prompt.choices": "none",
        "rule.line": border_style,
        "repr.path": darker_style,
        "repr.filename": darker_style,
        "status.spinner": "none",
        "progress.spinner": "none",
        "repr.number": "none",
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
