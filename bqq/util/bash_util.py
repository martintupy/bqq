import colorsys
import re
import shutil
import subprocess
import tempfile
from typing import Tuple

from bqq import const
from bqq.types import JobInfo
from prettytable.prettytable import PrettyTable

ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")


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
    width, height = get_size(message)
    cols = shutil.get_terminal_size().columns
    return width > cols or height > const.MAX_LINES


def get_size(message: str) -> Tuple[int, int]:
    escaped = ansi_escape.sub("", message)
    lines = escaped.split("\n")
    height = len(lines)
    width = len(max(lines, key=lambda x: len(x)))
    return width, height


def color_keywords(query: str) -> str:
    spaces = re.compile("[^\s]+").split(query)
    words = []
    for word in query.split():
        if word in const.BQ_KEYWORDS:
            words.append(hex_color(const.KEYWORD)(word))
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
