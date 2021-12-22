import sys
import time
import threading
import subprocess


class Spinner:
    busy = False
    delay = .05
    sequence = "▘▀▝▐▗▄▖▌"

    @staticmethod
    def spinning_cursor():
        while 1:
            for cursor in Spinner.sequence:
                yield cursor

    def __init__(self, delay=None):
        self.spinner_generator = self.spinning_cursor()
        if delay and float(delay):
            self.delay = delay

    def spinner_task(self):
        while self.busy:
            sys.stdout.write(next(self.spinner_generator))
            sys.stdout.flush()
            time.sleep(self.delay)
            sys.stdout.write("\b")
            sys.stdout.flush()

    def __enter__(self):
        self.busy = True
        subprocess.run(["tput", "civis"])
        threading.Thread(target=self.spinner_task).start()

    def __exit__(self, exception, value, tb):
        self.busy = False
        time.sleep(self.delay)
        subprocess.run(["tput", "cnorm"])
        if exception is not None:
            return False
