import csv
import glob
import os

from prettytable import PrettyTable
from prettytable.prettytable import ALL, MARKDOWN, MSWORD_FRIENDLY, NONE, PLAIN_COLUMNS

from bqq import const
from bqq.util import bash_util


def clear():
    files = glob.glob(f"/{const.BQQ_CSV}/*")
    for f in files:
        os.remove(f)


def write(id: str, header, rows):
    filename = f"{const.BQQ_CSV}/{id}.csv"
    with open(filename, "w") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)


def read(id: str) -> str:
    filename = f"{const.BQQ_CSV}/{id}.csv"
    table = bash_util.table()
    with open(filename) as f:
        reader = csv.reader(f, delimiter=",")
        header = reader.__next__()
        table.field_names = header
        for row in reader:
            table.add_row(row)
    table.align = "l"
    return table.get_string()
