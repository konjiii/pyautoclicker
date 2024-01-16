from backend import backend
import tkinter as tk
from tkinter import ttk
import os
from pynput import keyboard
import ctypes as ct

# create settings.txt if it doesn't exist
if not os.path.exists("settings.txt"):
    with open("settings.txt", "w") as f:
        f.write("click_interval=1000\n")
        # f.write("toggle_bind=keyboard.Key.f6\n")
        
class autoclicker(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.parent.resizable(False, False)
        self.configure_title_bar(self.parent)
        self.parent.title("AutoClicker")
        # if os.path.exists("theme\\theme.tcl"):
        #     self.parent.tk.call("source", "theme\\theme.tcl")
        #     self.parent.tk.call("set_theme", "dark")
        # self.parent.attributes("-alpha", 0.9)

        # self.toggle_key = eval(self.get_settings()["toggle_bind"])

        # initialize settings and backend
        self.settings = self.get_settings()
        self.backend = backend()

        # create the GUI
        self.frameinterval = ttk.LabelFrame(self.parent, text="Click interval")
        self.frameinterval.pack()

        self.linterval = ttk.Label(self.frameinterval, text="Click interval:")
        self.linterval.grid(row=0, column=0, padx=10, pady=10)

        self.interval_ms = tk.StringVar()
        self.interval_ms.set(self.settings["click_interval"])

        self.einterval = ttk.Entry(self.frameinterval, textvariable=self.interval_ms)
        self.einterval.grid(row=0, column=1, pady=10)
        # call update_interval() when enter is pressed
        self.einterval.bind("<Return>", lambda event: self.update_interval())

        self.lms = tk.Label(self.frameinterval, text="ms")
        self.lms.grid(row=0, column=2, padx=10, pady=10)

        self.framebinds = ttk.LabelFrame(self.parent, text="Keybinds")
        self.framebinds.pack()

        # self.bind_key = tk.StringVar()
        # self.bind_key.set(f"current keybind: F6")

        self.lbinds = ttk.Label(self.framebinds, text="current keybind: F6")
        self.lbinds.grid(row=0, column=0)

        # self.bbinds = ttk.Button(self.framebinds, text="Change keybinds", style="Accent.TButton", command=self.change_binds)
        # self.bbinds.grid(row=1, column=0, padx=10, pady=10)

        self.frametoggle = ttk.Frame(self.parent, padding=10)
        self.frametoggle.pack()

        self.toggle = tk.StringVar()
        self.toggle.set("Start")

        self.running = tk.BooleanVar()
        self.running.set(True)

        self.btoggle = ttk.Checkbutton(self.frametoggle, textvariable=self.toggle, style="Toggle.TButton", variable=self.running, command=self.toggle_loop_button)
        self.btoggle.grid(row=0, column=0)

        self.group = ttk.Labelframe

        # start the keyboard listener
        self.listener = keyboard.Listener(on_press=self.toggle_loop)
        self.listener.start()

    # update the click interval
    def update_interval(self) -> bool:
        if not self.interval_ms.get().isnumeric():
            self.interval_ms.set("invalid input")
            return False
        with open("settings.txt", "r") as f:
            lines = f.readlines()
        with open("settings.txt", "w") as f:
            for line in lines:
                if line.startswith("click_interval"):
                    f.write(f"click_interval={self.interval_ms.get()}\n")
                else:
                    f.write(line)
        return True

    def start_loop(self, button: bool):
        if self.update_interval():
            self.toggle.set("Stop")
            self.backend.start(int(self.interval_ms.get()), button)

    def stop_loop(self):
        self.toggle.set("Start")
        self.backend.stop()

    def toggle_loop_button(self):
        if self.running.get():
            self.stop_loop()
        else:
            self.start_loop(True)

    def toggle_loop(self, key):
        """keyboard listener"""
        if key == keyboard.Key.f6:
            self.running.set(not self.running.get())
            if self.running.get():
                self.stop_loop()
            else:
                self.start_loop(False)

    # def new_bind(self):
    #     self.listener.stop()
    #     self.listener = keyboard.Listener(on_press=self.toggle_loop)
    #     self.listener.start()
    #     self.bind_key.set(f"current keybind: {self.curr_bind.get()}")
    #     self.toggle_key = eval(self.curr_bind.get())
    #     self.top.destroy()
    #
    # def change_binds(self):
    #     """change the keybinds"""
    #     self.listener.stop()
    #
    #     self.top = tk.Toplevel(self.parent)
    #     self.top.title("Change keybinds")
    #     self.top.resizable(False, False)
    #     # self.top.grab_set()
    #     self.configure_title_bar(self.top)
    #
    #     self.framechange = ttk.Frame(self.top)
    #     self.framechange.pack()
    #
    #     self.lchange = ttk.Label(self.framechange, text="Press a key to change the keybind")
    #     self.lchange.pack(padx=10, pady=10)
    #
    #     self.curr_bind = tk.StringVar()
    #     self.curr_bind.set(self.settings["toggle_bind"])
    #
    #     def change_bind(key):
    #         self.curr_bind.set(key)
    #         self.top.focus()
    #
    #     self.listener = keyboard.Listener(on_press=change_bind)
    #     self.listener.start()
    #
    #     self.lcurr_bind = ttk.Label(self.framechange, textvariable=self.curr_bind)
    #     self.lcurr_bind.pack(padx=10, pady=10)
    #
    #     self.frameconfirmcancel = ttk.Frame(self.top)
    #     self.frameconfirmcancel.pack()
    #
    #     self.bconfirm_bind = ttk.Button(self.frameconfirmcancel, text="Confirm", style="Accent.TButton", command=self.new_bind)
    #     self.bconfirm_bind.grid(row=1, column=0, padx=10, pady=10)
    #
    #     # run this function when the popup window is closed
    #     def close_popup():
    #         self.listener.stop()
    #         self.listener = keyboard.Listener(on_press=self.toggle_loop)
    #         self.listener.start()
    #         self.top.destroy()
    #
    #     self.bcancel_bind = ttk.Button(self.frameconfirmcancel, text="Cancel", command=close_popup)
    #     self.bcancel_bind.grid(row=1, column=1, padx=10, pady=10)
    #
    #     self.top.protocol("WM_DELETE_WINDOW", close_popup)

    def get_settings(self) -> dict:
        """get the settings from settings.txt"""
        settings = {}
        # get the settings from settings.txt
        with open("settings.txt", "r") as f:
            for line in f.readlines():
                setting, value = line.split("=")
                settings[setting.strip()] = value.strip()

        if not settings["click_interval"].isnumeric():
            settings["click_interval"] = 1000
            with open("settings.txt", "w") as f:
                f.write(f"click_interval=1000\n")
                f.write(f"toggle_bind={settings['toggle_bind']}\n")

        return settings
    
    def configure_title_bar(self, window):
        """configure the title bar of the window"""
        window.update()
        DWMWA_USE_IMMERSIVE_DARK_MODE = 20
        set_window_attribute = ct.windll.dwmapi.DwmSetWindowAttribute
        get_parent = ct.windll.user32.GetParent
        hwnd = get_parent(window.winfo_id())
        rendering_policy = DWMWA_USE_IMMERSIVE_DARK_MODE
        value = 2
        value = ct.c_int(value)
        set_window_attribute(hwnd, rendering_policy, ct.byref(value), ct.sizeof(value))
        window.iconphoto(False, tk.PhotoImage(file="textures\\icon.png"))


if __name__ == "__main__":
    root = tk.Tk()
    app = autoclicker(root)
    root.mainloop()
    # kill the backend threads when the app is closed
    app.backend.kill()
    # stop the keyboard listener
    app.listener.stop()

