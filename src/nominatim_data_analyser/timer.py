from time import time

class Timer():
    def __init__(self, name: str) -> None:
        self.start_time = time()
        self.name = name

    @property
    def elapsed_str(self) -> str:
        hours, rem = divmod(time() - self.start_time, 3600)
        minutes, seconds = [int(round(t, 1)) for t in divmod(rem, 60)]

        if hours > 0:
            return f'{self.name} executed in {hours}h {minutes}min {seconds}s'
        if minutes > 0:
            return f'{self.name} executed in {minutes}min {seconds}s'

        return f'{self.name} executed in {seconds}s'
