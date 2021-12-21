import csv
import glob
import os
from pathlib import Path
from typing import Optional

from google.cloud.bigquery.table import RowIterator

from bqq import const
from bqq.service import bq_service
from bqq.types import JobInfo
from bqq.util import bash_util


def clear():
    files = glob.glob(f"/{const.BQQ_RESULTS}/*")
    for f in files:
        os.remove(f)


def ensure_project_dir(project: str):
    path = f"{const.BQQ_RESULTS}/{project}"
    Path(path).mkdir(exist_ok=True)


def write(project: str, id: str, rows: RowIterator):
    ensure_project_dir(project)
    filename = f"{const.BQQ_RESULTS}/{project}/{id}.csv"
    with open(filename, "w") as f:
        writer = csv.writer(f)
        header = [field.name for field in rows.schema]
        writer.writerow(header)
        for row in rows:
            writer.writerow(row)


def read(job_info: JobInfo) -> Optional[str]:
    filename = f"{const.BQQ_RESULTS}/{job_info.project}/{job_info.job_id}.csv"
    result = None
    if not os.path.isfile(filename):
        bq_service.download_result(job_info.job_id)
    if os.path.isfile(filename):
        table = bash_util.table()
        with open(filename) as f:
            reader = csv.reader(f, delimiter=",")
            header = reader.__next__()
            table.field_names = header
            for row in reader:
                table.add_row(row)
        table.align = "l"
        result = table.get_string()
    return result
