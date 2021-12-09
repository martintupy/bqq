import math


def size_fmt(num):
    for unit in ["B", "KB", "MB", "GB", "TB", "PB"]:
        if abs(num) < 1000:
            size = round(num, 1)
            return hex("D4BD1E")(f"{size}{unit}")
        else:
            num /= 1000


def price_fmt(num):
    tb = num / 1e12
    price = round(tb * 5, 2)
    return hex("D4BD1E")(f"{price}$")


def rgb(r: int, g: int, b: int):
    def inner(text):
        return f"\x1b[38;2;{r};{g};{b}m{text}\x1b[0m"

    return inner


def hex(hexstr: str):
    return rgb(*tuple(int(hexstr.lstrip("#")[i : i + 2], 16) for i in (0, 2, 4)))
