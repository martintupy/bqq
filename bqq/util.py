import subprocess
import tempfile


def size_fmt(num):
    for unit in ["B", "KB", "MB", "GB", "TB", "PB"]:
        if abs(num) < 1000:
            size = round(num, 1)
            return f"{size}{unit}"
        else:
            num /= 1000


def price_fmt(num):
    tb = num / 1e12
    price = round(tb * 5, 2)
    return f"${price}"


def rgb(r: int, g: int, b: int):
    def inner(text):
        return f"\x1b[38;2;{r};{g};{b}m{text}\x1b[0m"

    return inner


def hex_color(hexstr: str):
    return rgb(*tuple(int(hexstr.lstrip("#")[i : i + 2], 16) for i in (0, 2, 4)))


def fzf(choices: list):
    choices_str = "\n".join(map(str, choices))
    selection = None
    with tempfile.NamedTemporaryFile() as input_file:
        with tempfile.NamedTemporaryFile() as output_file:
            input_file.write(choices_str.encode("utf-8"))
            input_file.flush()
            cat = subprocess.Popen(["cat", input_file.name], stdout=subprocess.PIPE)
            subprocess.run(["fzf"], stdin=cat.stdout, stdout=output_file)
            cat.wait()
            with open(output_file.name) as f:
                selection = f.readline().strip("\n")
    return selection
