from pathlib import Path
import os
import yaml
from rich.style import Style
from rich.theme import Theme

# google-cloud-sdk oauth2 credentials
# https://github.com/twistedpair/google-cloud-sdk/blob/10fc3b9ccce1c13eb41a592faa6cc524610e8a16/google-cloud-sdk/lib/googlecloudsdk/core/config.py#L168-L169
# picked from tarball https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-367.0.0-linux-x86_64.tar.gz
CLOUDSDK_CLIENT_ID = "32555940559.apps.googleusercontent.com"
CLOUDSDK_CLIENT_NOTSOSECRET = "ZmssLNjJy2998hD4CTg2ejr2"

CLOUDSDK_CLIENT_ID = "32555940559.apps.googleusercontent.com"
CLOUDSDK_CLIENT_NOTSOSECRET = "ZmssLNjJy2998hD4CTg2ejr2"

SCOPE = "https://www.googleapis.com/auth/bigquery"

DEFAULT_BQQ_HOME = f"{Path.home()}/.bqq"

BQQ_HOME = os.getenv("BQQ_HOME", DEFAULT_BQQ_HOME)
BQQ_RESULTS = f"{BQQ_HOME}/results"
BQQ_SCHEMAS = f"{BQQ_HOME}/schemas"
BQQ_INFOS = f"{BQQ_HOME}/infos.json"
BQQ_CONFIG = f"{BQQ_HOME}/config.yaml"

BQQ_DISABLE_COLORS = os.getenv("BQQ_DISABLE_COLORS", "False").lower() in ("true", "1", "t")
BQQ_SKIN = os.getenv("BQQ_SKIN")

default_skin = {
    "question": "yellow3",
    "info": "green",
    "error": "red",
    "warning": "gold3",
    "border": "grey27",
    "darker": "grey46",
    "alternate": "grey50",
    "link": "light_sky_blue1",
    "keyword": "dodger_blue1",
}

skin = default_skin

if BQQ_SKIN and os.path.isfile(BQQ_SKIN):
    bqq_skin = yaml.safe_load(open(BQQ_SKIN, "r"))
    skin = {**skin, **bqq_skin}

question_style = Style(color=skin["question"])
info_style = Style(color=skin["info"])
warning_style = Style(color=skin["warning"])
error_style = Style(color=skin["error"])
border_style = Style(color=skin["border"])
darker_style = Style(color=skin["darker"])
alternate_style = Style(color=skin["alternate"])
link_style = Style(color=skin["link"])
keyword_style = Style(color=skin["keyword"])

theme = Theme(
    {
        "progress.elapsed": darker_style,
        "prompt.default": darker_style,
        "prompt.choices": "default",
        "rule.line": border_style,
        "repr.path": darker_style,
        "repr.filename": darker_style,
        "status.spinner": "none",
        "progress.spinner": "none",
        "repr.number": "none",
    }
)

FZF_SEPARATOR = " ~ "

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
