import tkinter as tk


# tk.Scale

class InputRange(tk.Frame):
    """
    数值滑动框，只占一行
    """

    def __init__(self, title: str, from_, to, *args, **kwargs):
        """
        :param title: 滑动框左侧的标题
        :param args:
        :param kwargs:
        """
        self.value = kwargs.pop('variable', None)

        super(InputRange, self).__init__(*args, **kwargs)

        self.label = tk.Label(self, text=title)
        self.label.config(
            fg='white',
            bg='#2e3e26'
        )
        self.label.pack(side=tk.LEFT)

        self.scale = tk.Scale(self, from_=from_, to=to, orient="horizontal")
        self.scale.config(
            fg='white',
            bg='#2e3e26',
            highlightbackground='#2e3e26',  # 隐藏白色边框
            activebackground='#7fff00',  # 设置滑动条在悬停状态下的背景颜色为浅绿色
            troughcolor='#006400'  # 设置滑动条的条内背景颜色为深绿色
        )
        self.scale.pack(side=tk.LEFT)

        self.config(
            bg='#2e3e26'
        )
        self.pack()

        if self.value is not None:
            self.scale.config(variable=self.value)
            self.value.set(self.scale.get())

        # label = tk.Label(self, text="线条不透明度（%）:")
        # label.pack(padx=10, pady=20)
        # self.pack(padx=20, pady=20)

        # label = tk.Label(self.master, text="线条不透明度（%）:")
        # label.grid(row=0, column=0, padx=10, pady=20)
        # self.grid(row=1, column=0, padx=20, pady=20)
