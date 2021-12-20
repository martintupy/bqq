import csv
import glob
import os

from prettytable import PrettyTable

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


def read(id: str) -> PrettyTable:
    filename = f"{const.BQQ_CSV}/{id}.csv"
    table = PrettyTable()
    table.vertical_char = bash_util.hex_color(const.TABLE_BORDER)("|")
    table.horizontal_char = bash_util.hex_color(const.TABLE_BORDER)("-")
    table.junction_char = bash_util.hex_color(const.TABLE_BORDER)("+")
    with open(filename) as f:
        reader = csv.reader(f, delimiter=",")
        header = reader.__next__()
        table.field_names = [bash_util.hex_color(const.TABLE_HEADER)(field) for field in header]
        for row in reader:
            table.add_row(row)

    table.align = "l"
    return table
