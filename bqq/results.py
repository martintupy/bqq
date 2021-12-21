import csv
import glob
import os
import click

from bqq import const
from bqq.types import JobInfo
from bqq.util import bash_util
from bqq.service import bq_service
from pathlib import Path


def clear():
    files = glob.glob(f"/{const.BQQ_RESULTS}/*")
    for f in files:
        os.remove(f)


def ensure_project_dir(project: str):
    path = f"{const.BQQ_RESULTS}/{project}"
    Path(path).mkdir(exist_ok=True)


def write(project: str, id: str, header, rows):
    ensure_project_dir(project)
    filename = f"{const.BQQ_RESULTS}/{project}/{id}.csv"
    with open(filename, "w") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for row in rows:
            writer.writerow(row)


def read(job_info: JobInfo) -> str:
    filename = f"{const.BQQ_RESULTS}/{job_info.project}/{job_info.job_id}.csv"
    table = bash_util.table()
    if not os.path.isfile(filename):
        bq_service.download_result(job_info.job_id)
    if os.path.isfile(filename):
        with open(filename) as f:
            reader = csv.reader(f, delimiter=",")
            header = reader.__next__()
            table.field_names = header
            for row in reader:
                table.add_row(row)
        table.align = "l"
    return table.get_string()
