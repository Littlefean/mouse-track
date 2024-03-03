import tkinter as tk


class Radio(tk.Checkbutton):
    def __init__(self, *args, **kwargs):
        super(Radio, self).__init__(*args, **kwargs)
        self.pack(pady=2)
