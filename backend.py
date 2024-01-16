import win32api, win32con
import threading
from threading import Event

class backend:
    def __init__(self):
        self.exit = Event()

    def loop(self, interval_ms: int):
        """the click loop"""
        while not self.exit.is_set():
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
            self.exit.wait(interval_ms / 1000)

    def loop_button(self, interval_ms: int):
        """the click loop"""
        self.exit.wait(1)
        while not self.exit.is_set():
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
            self.exit.wait(interval_ms / 1000)

    def start(self, interval_ms: int, button: bool):
        """starts the click loop"""
        self.exit.clear()
        if button:
            t1 = threading.Thread(target=self.loop_button, args=(interval_ms,))
            t1.start()
        else:
            t1 = threading.Thread(target=self.loop, args=(interval_ms,))
            t1.start()

    def stop(self):
        """stops the click loop"""
        self.exit.set()

    def kill(self):
        """kill all threads"""
        # self.exit the wait in loop()
        self.exit.set()

