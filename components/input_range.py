import tkinter as tk


class InputRange(tk.Scale):
    """
    数值滑动框
    """

    def __init__(self, *args, **kwargs):
        self.value = kwargs.pop('variable', None)
        super(InputRange, self).__init__(*args, **kwargs)
        if self.value is not None:
            self.config(variable=self.value)
            self.value.set(self.get())

        self.pack(side="left", padx=20, pady=20)
