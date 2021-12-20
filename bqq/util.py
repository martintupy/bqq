import shutil
import subprocess
import tempfile
import colorsys
import sqlparse
import re

from prettytable.prettytable import PrettyTable
from bqq.data import Metadata

from bqq.const import BQ_KEYWORDS, DARKER, KEYWORD, MAX_LINES, TABLE_BORDER, TABLE_HEADER


def size_fmt(num):
    for unit in ["B", "KiB", "MiB", "GiB", "TiB", "PiB"]:
        if abs(num) < 1024:
            size = round(num, 1)
            return f"{size} {unit}"
        else:
            num /= 1024


def price_fmt(num):
    tb = num / 1e12
    price = round(tb * 5, 2)
    return f"{price} $"


def rgb(r: int, g: int, b: int):
    def inner(text: str) -> str:
        return f"\x1b[38;2;{r};{g};{b}m{text}\x1b[0m"

    return inner


def hex_color(hexstr: str, amount=1.0):
    r, g, b = tuple(int(hexstr.lstrip("#")[i : i + 2], 16) for i in (0, 2, 4))
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    rr, gg, bb = colorsys.hls_to_rgb(h, l * amount, s)
    return rgb(int(rr), int(gg), int(bb))


def use_less(message: str) -> bool:
    height = len(message.split("\n"))
    width = len(max(message.split("\n")))
    cols = shutil.get_terminal_size().columns
    width > cols or height > MAX_LINES


def result_header(metadata: Metadata) -> str:
    sql = sqlparse.format(metadata.query, reindent=True)
    return (
        hex_color(TABLE_HEADER)("Execution time")
        + f" = {metadata.datetime}\n"
        + color_keywords(sql)
    )


def color_keywords(query: str) -> str:
    spaces = re.compile("[^\s]+").split(query)
    words = []
    for word in query.split():
        if word in BQ_KEYWORDS:
            words.append(hex_color(KEYWORD)(word))
        else:
            words.append(word)
    return "".join(["".join(map(str, i)) for i in zip(spaces, words)])


def fzf(choices: list):
    choices_str = "\n".join(map(str, choices))
    selection = None
    with tempfile.NamedTemporaryFile() as input_file:
        with tempfile.NamedTemporaryFile() as output_file:
            input_file.write(choices_str.encode("utf-8"))
            input_file.flush()
            cat = subprocess.Popen(["cat", input_file.name], stdout=subprocess.PIPE)
            subprocess.run(["fzf", "--ansi"], stdin=cat.stdout, stdout=output_file)
            cat.wait()
            with open(output_file.name) as f:
                selection = f.readline().strip("\n")
    return selection
