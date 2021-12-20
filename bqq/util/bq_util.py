def size_fmt(num: int) -> str:
    for unit in ["B", "KiB", "MiB", "GiB", "TiB", "PiB"]:
        if abs(num) < 1024:
            size = round(num, 1)
            return f"{size} {unit}"
        else:
            num /= 1024


def price_fmt(num: int) -> str:
    tb = num / 1e12
    price = round(tb * 5, 2)
    return f"{price} $"