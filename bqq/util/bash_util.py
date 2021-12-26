import re
import shutil
import subprocess
import tempfile
import itertools
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
        if fg and not const.BQQ_DISABLE_COLORS:
            text = rgb_fg(*tuple(int(fg.lstrip("#")[i : i + 2], 16) for i in (0, 2, 4)))(text)
        if bg and not const.BQQ_DISABLE_COLORS:
            text = rgb_bg(*tuple(int(bg.lstrip("#")[i : i + 2], 16) for i in (0, 2, 4)))(text)
        return text

    return inner


def use_less(message: str) -> bool:
    lines = escape_ansi(message).split("\n")
    height = len(lines)
    width = len(max(lines, key=lambda x: len(x)))
    cols = shutil.get_terminal_size().columns
    return width > cols or height > const.BQQ_MAX_LINES


def escape_ansi(message: str) -> str:
    ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
    return ansi_escape.sub("", message)


def get_max_width(messages: List[str]) -> int:
    lines2d = [escape_ansi(message).split("\n") for message in messages]
    lines = list(itertools.chain(*lines2d))
    width = len(max(lines, key=lambda x: len(x)))
    cols = shutil.get_terminal_size().columns
    return min(width, cols)


def color_keywords(query: str) -> str:
    spaces = re.compile("[^\s]+").split(query)
    words = []
    for word in query.split():
        if word in const.BQ_KEYWORDS:
            words.append(hex_color(const.KEYWORD)(word))
        else:
            words.append(word)
    return "".join(["".join(map(str, i)) for i in zip(spaces, words)])


def fzf(choices: List[str], multi=False) -> List[str]:
    choices.sort(reverse=True, key=_fzf_key)
    choices_str = "\n".join(map(str, choices))
    selection = []
    multi = "--multi" if multi else None
    fzf_args = filter(None, ["fzf", "--ansi", multi])
    with tempfile.NamedTemporaryFile() as input_file:
        with tempfile.NamedTemporaryFile() as output_file:
            input_file.write(choices_str.encode("utf-8"))
            input_file.flush()
            cat = subprocess.Popen(["cat", input_file.name], stdout=subprocess.PIPE)
            subprocess.run(fzf_args, stdin=cat.stdout, stdout=output_file)
            cat.wait()
            with open(output_file.name) as f:
                selection = [line.strip("\n") for line in f.readlines()]
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


class no_wrap:
    def __enter__(self):
        subprocess.run(["tput", "rmam"])

    def __exit__(self, exception, value, tb):
        subprocess.run(["tput", "smam"])
