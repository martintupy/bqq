import csv
import glob
import os
from pathlib import Path
from typing import Union
import shutil

from google.cloud.bigquery.table import RowIterator
from rich import box

from bqq import const
from bqq.types import JobInfo
from rich.table import Table, Text


class Results:
    def __init__(self) -> None:
        pass

    def clear(self):
        dirs = glob.glob(f"{const.BQQ_RESULTS}/*")
        for dir in dirs:
            shutil.rmtree(dir)

    def ensure_project_dir(self, project: str):
        path = f"{const.BQQ_RESULTS}/{project}"
        Path(path).mkdir(exist_ok=True)

    def write(self, project: str, id: str, rows: RowIterator):
        self.ensure_project_dir(project)
        filename = f"{const.BQQ_RESULTS}/{project}/{id}.csv"
        with open(filename, "w") as f:
            writer = csv.writer(f)
            header = [field.name for field in rows.schema]
            writer.writerow(header)
            for row in rows:
                writer.writerow(row)

    def read(self, job_info: JobInfo) -> Union[None, Text, Table]:
        filename = f"{const.BQQ_RESULTS}/{job_info.project}/{job_info.job_id}.csv"
        result = None
        if os.path.isfile(filename):
            table = Table(box=box.ROUNDED, border_style="dim")
            with open(filename) as f:
                reader = csv.reader(f, delimiter=",")
                header = reader.__next__()
                table.add_column()
                for col in header:
                    table.add_column(col)
                for i, row in enumerate(reader):
                    table.add_row(Text(f"{i}", style="dim"), *row)
            result = table
        return result
