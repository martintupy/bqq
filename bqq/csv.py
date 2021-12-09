import csv
from uuid import UUID

from prettytable import PrettyTable

from bqq.const import BQQ_CSV, TABLE_BORDER, TABLE_HEADER
from bqq.util import hex


def write_csv(id: str, header, rows):
    filename = f"{BQQ_CSV}/{id}.csv"
    with open(filename, "w") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)


def read_csv(id: UUID) -> PrettyTable:
    filename = f"{BQQ_CSV}/{id}.csv"
    table = PrettyTable()
    table.vertical_char = hex(TABLE_BORDER)("|")
    table.horizontal_char = hex(TABLE_BORDER)("-")
    table.junction_char = hex(TABLE_BORDER)("+")
    with open(filename) as f:
        reader = csv.reader(f, delimiter=",")
        header = reader.__next__()
        table.field_names = [hex(TABLE_HEADER)(field) for field in header]
        for row in reader:
            table.add_row(row)

    table.align = "l"
    return table
