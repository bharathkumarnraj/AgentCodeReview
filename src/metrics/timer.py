import time


class Timer:

    def __init__(self):
        self.start_time = None
        self.end_time = None

    def start(self):
        self.start_time = time.perf_counter()

    def stop(self):
        self.end_time = time.perf_counter()

    @property
    def elapsed(self):
        if self.start_time is None or self.end_time is None:
            return 0.0

        return self.end_time - self.start_time