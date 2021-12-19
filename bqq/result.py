import csv

from prettytable import PrettyTable

from bqq.const import BQQ_CSV, TABLE_BORDER, TABLE_HEADER
from bqq.util import hex_color
import os
import glob


def clear():
    files = glob.glob(f"/{BQQ_CSV}/*")
    for f in files:
        os.remove(f)


def write(date: str, header, rows):
    filename = f"{BQQ_CSV}/{date}.csv"
    with open(filename, "w") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)


def read(date: str) -> PrettyTable:
    filename = f"{BQQ_CSV}/{date}.csv"
    table = PrettyTable()
    table.vertical_char = hex_color(TABLE_BORDER)("|")
    table.horizontal_char = hex_color(TABLE_BORDER)("-")
    table.junction_char = hex_color(TABLE_BORDER)("+")
    with open(filename) as f:
        reader = csv.reader(f, delimiter=",")
        header = reader.__next__()
        table.field_names = [hex_color(TABLE_HEADER)(field) for field in header]
        for row in reader:
            table.add_row(row)

    table.align = "l"
    return table
