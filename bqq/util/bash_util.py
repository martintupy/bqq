import re
import shutil
import subprocess
import tempfile
from typing import List, Tuple

from bqq import const
from prettytable.prettytable import PrettyTable


def rgb_fg(r: int, g: int, b: int):
    def inner(text: str) -> str:
        return f"\x1b[38;2;{r};{g};{b}m{text}\x1b[0m"

    return inner


def rgb_bg(r: int, g: int, b: int):
    def inner(text: str) -> str:
        return f"\x1b[48;2;{r};{g};{b}m{text}\x1b[0m"

    return inner


def hex_color(fg: str = None, bg: str = None):
    def inner(text: str) -> str:
        if fg:
            text = rgb_fg(*tuple(int(fg.lstrip("#")[i : i + 2], 16) for i in (0, 2, 4)))(text)
        if bg:
            text = rgb_bg(*tuple(int(bg.lstrip("#")[i : i + 2], 16) for i in (0, 2, 4)))(text)
        return text

    return inner


def use_less(message: str) -> bool:
    width, height = get_size(message)
    cols = shutil.get_terminal_size().columns
    return width > cols or height > const.MAX_LINES


def escape_ansi(message: str) -> str:
    ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
    return ansi_escape.sub("", message)


def get_size(message: str) -> Tuple[int, int]:
    lines = escape_ansi(message).split("\n")
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


def fzf(choices: List[str]) -> str:
    choices.sort(reverse=True, key=_fzf_key)
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


def _fzf_key(line: str) -> str:
    escaped = escape_ansi(line)
    return escaped.split(const.FZF_SEPARATOR)[0]


def table() -> PrettyTable:
    table = PrettyTable()
    table.top_junction_char = hex_color(const.DARKER)("┳")
    table.top_left_junction_char = hex_color(const.DARKER)("┏")
    table.top_right_junction_char = hex_color(const.DARKER)("┓")
    table.bottom_junction_char = hex_color(const.DARKER)("┻")
    table.bottom_left_junction_char = hex_color(const.DARKER)("┗")
    table.bottom_right_junction_char = hex_color(const.DARKER)("┛")
    table.left_junction_char = hex_color(const.DARKER)("┣")
    table.right_junction_char = hex_color(const.DARKER)("┫")
    table.vertical_char = hex_color(const.DARKER)("┃")
    table.horizontal_char = hex_color(const.DARKER)("━")
    table.junction_char = hex_color(const.DARKER)("╋")
    return table
