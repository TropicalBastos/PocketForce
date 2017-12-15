import time
import threading

__MILLISECOND__ = 0.001
total_elapsed = 0.0

class StopwatchThreadInterface(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.elapsed = 0.0
        self.running = False
        self.class_thread = threading.Thread()


    def get_time(self, raw = False):
        global total_elapsed
        if raw:
            return total_elapsed
        return "%.1fs" % total_elapsed

    def run(self):
        global total_elapsed
        self.running = True
        starttime = time.time()
        while self.running:
            time.sleep(__MILLISECOND__ - ((time.time() - starttime) % __MILLISECOND__))
            total_elapsed += __MILLISECOND__

    def stop(self):
        self.running = False

    def reset(self):
        global total_elapsed
        if self.running:
            print("Please stop the stopwatch before resetting")
            exit()
        total_elapsed = 0.0

