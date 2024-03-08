import tkinter as tk


class Radio(tk.Checkbutton):
    def __init__(self, *args, **kwargs):
        super(Radio, self).__init__(*args, **kwargs)
        self.config(
            bg='#2e3e26',  # 没有透明，要和背景保持一致
            # fg='white',
            foreground='white',
            # highlightbackground='red',
            # highlightcolor='blue',
            selectcolor='#182015',
            activebackground='#3f5235',
            activeforeground='#b8e3a3',
        )
        self.pack(pady=2)
