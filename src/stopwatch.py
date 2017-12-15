import time
import threading
from stopwatch_thread_interface import StopwatchThreadInterface

class Stopwatch():

    def __init__(self):
        self.thread_stopped = False
        self.interface = StopwatchThreadInterface()

    def get_time(self, raw = False):
        return self.interface.get_time(raw)

    def start(self):
        if self.thread_stopped:
            self.interface = StopwatchThreadInterface()
        self.interface.start()

    def stop(self):
        self.interface.stop()
        self.thread_stopped = True

    def reset(self):
        self.interface.reset()
