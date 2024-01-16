import backend
from tkinter import *
from tkinter import messagebox
import time
import keyboard
import win32api, win32con
import os

if not os.path.exists("settings.txt"):
    with open("settings.txt", "w") as f:
        f.write("click_interval=1000\n")

def update_interval():
    global interval_ms
    if not interval_ms.get().isnumeric():
        interval_ms.set("invalid input")
        return
    with open("settings.txt", "r") as f:
        lines = f.readlines()
    with open("settings.txt", "w") as f:
        for line in lines:
            if line.startswith("click_interval"):
                f.write(f"click_interval={interval_ms.get()}\n")
            else:
                f.write(line)
    return

def start_loop():
    bstart.config(relief=SUNKEN)
    bstart.config(state=DISABLED)
    bstop.config(relief=RAISED)
    bstop.config(state=NORMAL)
    backend.start(int(interval_ms.get()))
    return

def stop_loop():
    bstop.config(relief=SUNKEN)
    bstop.config(state=DISABLED)
    bstart.config(relief=RAISED)
    bstart.config(state=NORMAL)
    backend.stop()
    return

with open("settings.txt", "r") as f:
    ms = f.read().split("=")[1].strip()
    if not ms.isnumeric():
        messagebox.showerror("Error", "Invalid click interval in settings.txt")
        exit()

tk = Tk()

linterval = Label(tk, text="Click interval:")
linterval.grid(row=0, column=0)

interval_ms = StringVar()
interval_ms.set(ms)
einterval = Entry(tk, textvariable=interval_ms)
einterval.grid(row=0, column=1)

lms = Label(tk, text="ms")
lms.grid(row=0, column=2)

einterval.bind("<Return>", lambda event: update_interval())

bupdate = Button(tk, text="Update", command=update_interval)
bupdate.grid(row=0, column=3)

bstart = Button(tk, text="Start", command=start_loop)
bstart.grid(row=1, column=0)

bstop = Button(tk, text="Stop", command=stop_loop)
bstop.grid(row=1, column=1)
bstop.config(relief=SUNKEN)
bstop.config(state=DISABLED)

tk.mainloop()
backend.stop()

