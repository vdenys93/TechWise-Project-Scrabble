import time
import datetime


class Timer:

    def __init__(self):
        self._start_time = datetime.time(0,0)
        self._now = datetime.time()


    def reset(self):
        self._start_time = datetime.time(0,0)

    def start(self):
        self._start_time = datetime.now()

    def get_timer(self) -> str:
        if self._start_time is not None:
            return str(self._now - self._start_time)
        else: return "0"
