import threading

import time


class Weather(threading.Thread):
    def __init__(self):
        super().__init__()
        self.tx = "default"

    def run(self):
        i = 0
        while True:
            print(str(i + 1) + self.tx)
            time.sleep(1)

    def set(self, t):
        self.tx = t


if __name__ == '__main__':
    w=Weather()
    w.start()
    time.sleep(3)
    w.set("wllah")