from __future__ import annotations
from typing import Tuple
from time import time

class Timer():
    def __init__(self) -> None:
        self.start_time = 0.0

    def start_timer(self) -> Timer:
        self.start_time = time()
        return self

    def get_elapsed(self) -> Tuple[int, int]:
        hours, rem = divmod(time() - self.start_time, 3600)
        minutes, seconds = divmod(rem, 60)
        return int(round(minutes, 1)), int(round(seconds, 1))
