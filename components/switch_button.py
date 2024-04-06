import tkinter as tk
from typing import List, Callable


class SwitchButton(tk.Button):
    """
    具有多阶段循环状态切换的按钮
    例如2状态切换按钮：
     startRecord────►stopRecord
      ▲              │
      │              │
      └──────────────┘
    这个便是目前项目中使用的按钮。
    为了可扩展性，可以有两个以上的状态阶段。

     state1───►state2────►tate3───►state4
       ▲                             │
       └─────────────────────────────┘
    """

    def __init__(self, command_list: List[Callable], text_list: List[str], *args, **kwargs):
        """

        :param command_list: 每一个状态的点击触发函数 组成的数组
        :param text_list: 需要将每一个状态对应的按钮名称写成一个数组
        :param args:
        :param kwargs:
        """
        kwargs["cursor"] = "hand2"
        super(SwitchButton, self).__init__(*args, **kwargs)
        if not command_list or not text_list:
            raise Exception('状态列表长度不能为0')
        if len(command_list) != len(text_list):
            raise Exception('状态列表长度和状态列表名称长度不相等')

        self.click_count = 0
        self.text_list = text_list

        # 绑定所有的点击事件
        self.command_list = command_list

        self.config(
            bg='#b8e3a3',
            fg='black',
            text=self.text_list[0],
            command=self.onclick
        )
        self.pack(pady=10)
        # self.grid(row=3, column=0, padx=20, pady=20)

    def onclick(self):
        current_index = self.click_count % len(self.command_list)
        self.command_list[current_index]()

        self.click_count += 1

        self.config(text=self.text_list[self.click_count % len(self.command_list)])

    pass
