import time
import win32api, win32con
import time
import threading
import keyboard

running = False

def loop(interval_ms):
    global running
    while running:
        # win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
        # win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
        print("click")
        time.sleep(interval_ms/1000)

def start(interval_ms):
    global running
    running = True
    time.sleep(1)
    t1 = threading.Thread(target=loop, args=(interval_ms,))
    t1.start()

def stop():
    global running
    running = False

def keybinds(interval_ms):
    while True:
        if keyboard.is_pressed("F6"):
            start(interval_ms)
        elif keyboard.is_pressed("F6"):
            stop()
        time.sleep(0.1)

