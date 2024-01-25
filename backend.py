import win32api, win32con
import threading
from threading import Event
import time

class backend:
    def __init__(self):
        self.exit = Event()
        self.active = False
        self.t1 = None

    def loop(self, interval_ms: int, button: bool):
        """the click loop"""
        if button:
            self.exit.wait(1)

        while not self.exit.is_set():
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
            # use self.exit.wait instead of time.sleep so it can be stopped
            self.exit.wait(interval_ms / 1000)

    def fast_loop(self, interval_ms: int, button: bool):
        """the faster click loop"""
        if button:
            self.exit.wait(1)

        while self.active:
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
            time.sleep(interval_ms / 1000)

    def start(self, interval_ms: int, button: bool):
        """starts the click loop"""
        # if the interval is smaller than 20ms, use the fast loop since
        # self.exit.wait is slower than time.sleep
        if interval_ms > 20:
            self.exit.clear()
            self.t1 = threading.Thread(target=self.loop, args=(interval_ms, button))
            self.t1.start()
        else:
            self.exit.clear()
            self.active = True
            self.t1 = threading.Thread(target=self.fast_loop, args=(interval_ms, button))
            self.t1.start()

    def stop(self):
        """stops the click loop"""
        self.exit.set()
        self.active = False
        if not self.t1 is None:
            self.t1.join()

