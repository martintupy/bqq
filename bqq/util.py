import math


def num_fmt(num, suffix="B"):
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"


def rgb(r: int, g: int, b: int):
    def inner(text):
        return f"\x1b[38;2;{r};{g};{b}m{text}\x1b[0m"

    return inner


def hex(hexstr: str):
    return rgb(*tuple(int(hexstr.lstrip("#")[i : i + 2], 16) for i in (0, 2, 4)))
