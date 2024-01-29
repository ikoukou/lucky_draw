#!/usr/bin/env python
# encoding: utf-8
import datetime
import os
import tkinter
from os import path
from tkinter import font, messagebox
import time
import threading
import random
import pandas as pd
from PIL import ImageTk, Image
import sys
from configs import envir_config as env
from utils.awards_list import get_awards_list, get_awards_total, get_index
from utils.num_trans import arabic_to_chinese


class LuckyDraw:
    def __init__(self, namelist):
        # 准备好界面，使用当前屏幕100%的大小构建初试窗口
        self.root = tkinter.Tk()
        self.root.title("2024 天津园区年会抽奖")
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.root.geometry('{}x{}+0+0'.format(self.screen_width, self.screen_height))
        self.root.resizable(False, False)

        self.image_back = Image.open(env["image_background"]).resize((self.screen_width, self.screen_height))
        self.im = ImageTk.PhotoImage(self.image_back)
        background_label = tkinter.Label(self.root, image=self.im)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # 直接拉伸到占满屏幕
        # self.canvas.create_image(self.screen_width / 2, self.screen_height / 2, image=self.im)
        # self.canvas.pack()

        # 设置全局字体
        font_root = font.Font(family="微软雅黑", size=env["font_size_button"], weight="bold")

        # 构建抽奖按钮，绑定到new_task
        self.label_start = tkinter.Button(self.root, text="开冲！", font=font_root, bg="gray", foreground="white")
        self.label_start.place(x=self.screen_width * 0.05,
                               y=self.screen_height * 0.8 - (env["award_button_height"] + 20) * 1,
                               width=env["award_button_width"], height=env["award_button_height"])
        self.label_start.bind("<Button-1>", self.new_task)

        # 获取target名字的列表，以及奖品信息的数组字典
        self.target_name_list = get_awards_list(env["awards_tuple"])
        self.awards_tuple = env["awards_tuple"]
        color_list = [
            "blue",
            "brown",
            "yellow",
            "green",
            "red",
            "gray",
            "orange"
        ]

        # 按奖品信息数组字典的信息，批量创建各奖项的抽奖按钮
        tmp = 1
        for award in self.awards_tuple[::-1]:
            tmp += 1
            setattr(self, "button" + str(award["id"]),
                    tkinter.Button(self.root, text=arabic_to_chinese(int(award["id"])) + "等奖",
                                   font=font_root, bg=color_list[-int(award["id"])], foreground="white"))
            getattr(self, "button" + str(award["id"])).place(
                x=self.screen_width * 0.05,
                y=self.screen_height * 0.8 - (env["award_button_height"] + 20) * tmp,
                width=env["award_button_width"],
                height=env["award_button_height"])
            getattr(self, "button" + str(award["id"])).bind("<Button-1>", getattr(self, "set" + str(award["id"])))

        # 声明一个是否按下开始的变量
        self.isloop = False
        self.newloop = False

        self.data = namelist

        # 定义字体和跳动窗口
        font_target = font.Font(family="微软雅黑", size=env["font_size_target"], weight="bold")
        self.btn1 = tkinter.Text(self.root, font=("微软雅黑", env["font_size_target"]))
        self.btn1.place(x=self.screen_width * 0.5, y=self.screen_height * 0.2,
                        width=200, height=self.screen_height * 0.6)
        # 当前可抽选人员列表
        self.source = tkinter.Text(self.root, bg="navajowhite", fg="dimgray")
        self.source.insert(tkinter.END, "、".join(self.data))

        # 声明各个奖项获奖人员名单文本框
        self.target_dict = {}
        for tar in self.target_name_list:
            setattr(self, tar, tkinter.Listbox(self.root, height=5, font=font_target, bg='gray', bd=1, fg='white'))
            self.target_dict[getattr(self, tar)] = tar

        # 声明获奖名单的显示和隐藏按钮
        self.button_show = tkinter.Button(self.root, text="显示/隐藏 中奖名单", font=font_target,
                                          command=self.show_listbox)
        self.button_show.place(x=self.screen_width * 0.05, y=self.screen_height * 0.8,
                               width=env["award_button_width"], height=env["award_button_height"])

        self.show = False

        self.target = getattr(self, self.target_name_list[-1])
        self.root.mainloop()

    def show_listbox(self):
        self.show = not self.show
        max_count = max([item["count"] for award in env["awards_tuple"] for item in award["awards_list"]])
        for target in self.target_dict.keys():
            target.place_forget()
        if self.show:
            # 计算元素总高度，与屏幕高度做比较
            total_height = 0
            for i in range(1, len(self.awards_tuple) + 1):
                height = (env["font_size_target"] * 2) * self.awards_tuple[i - 1]["awards_list"][0]["count"]
                total_height += height + 20
            # 当屏幕高度比总元素高度小时，等比例缩小布局
            if self.screen_height < total_height:
                pass
            # 当屏幕高度比总元素高度大时，正常布局
            else:
                cur_y = 0
                for i in range(1, len(self.awards_tuple) + 1):
                    height = (env["font_size_target"] * 2) * self.awards_tuple[i - 1]["awards_list"][0]["count"]
                    y = (self.screen_height - total_height) / 2 + cur_y
                    for j in range(max_count):
                        target_name = f"target_{i}-{j}"
                        if target_name in self.target_name_list:
                            # 相对靠左侧L型布局
                            x = self.screen_width * 0.6 + (env["target_persons_width"] + 20) * j
                            # 相对靠右侧反L型布局
                            x = self.screen_width - (env["target_persons_width"] + 20) * (j + 1)
                            getattr(self, target_name).place(x=x, y=y, width=env["target_persons_width"],
                                                             height=height)
                    cur_y += height + 20

    def get_next_target_name(self):
        f, s = get_index(self.target_dict.get(self.target))
        if f"target_{f}-{s - 1}" in self.target_name_list:
            return f"target_{f}-{s - 1}"

    def rounds(self):
        # 判断是否开始循环
        if self.isloop:
            return

        # 死循环
        while True:
            if self.newloop:
                self.newloop = False
                f, s = get_index(self.target_dict.get(self.target))
                if self.target.size() >= self.awards_tuple[f - 1]["awards_list"][s]["count"]:
                    target_name = self.get_next_target_name()
                    if target_name:
                        self.target = getattr(self, target_name)
                    else:
                        messagebox.showinfo('提示', "本轮抽奖结束!")
                        return
                if isinstance(temp, list):
                    for i in temp:
                        self.target.insert(tkinter.END, i.center(5, " "))
                        self.data.remove(i)
                else:
                    self.target.insert(tkinter.END, temp.center(5, " "))
                    self.data.remove(temp)
                self.source.delete(1.0, 'end')
                self.source.insert(tkinter.END, "、".join(self.data))
                # 检查所有奖项是否全部抽完
                end = True
                for target_name in self.target_name_list:
                    f, s = get_index(target_name)
                    if getattr(self, target_name).size() < self.awards_tuple[f - 1]["awards_list"][s]["count"]:
                        end = False
                if end:
                    last_list = self.data
                    with open('last_list_{}.txt'.format(str(datetime.datetime.now().strftime("%m%d%H%M"))),
                              'w') as file:
                        for item in last_list:
                            file.write(str(item) + '\n')
                return

            # 延时操作
            time.sleep(0.1)
            f, s = get_index(self.target_dict.get(self.target))
            count = 1 if self.awards_tuple[f - 1]["awards_list"][s]["count"] < 5 \
                else self.awards_tuple[f - 1]["awards_list"][s]["count"]
            temp = random.sample(self.data, count)
            self.btn1.delete("1.0", tkinter.END)
            for string in temp:
                self.btn1.insert(tkinter.END, string + "\n")
            self.btn1.tag_configure("center", justify="center")
            self.btn1.tag_add("center", "1.0", "end")
            self.btn1.config(spacing1=40)

    # 建立一个新线程的函数
    def new_task(self, event):
        if not self.isloop:
            t = threading.Thread(target=self.rounds)
            t.start()
            self.isloop = True
        elif self.isloop:
            self.isloop = False
            self.newloop = True

    def set5(self, event):
        num = 5
        self.get_award_window(num)
        for i in range(len(env["awards_tuple"][num - 1]["awards_list"]) - 1, -1, -1):
            if getattr(self, f"target_{num}-{i}").size() >= env["awards_tuple"][num - 1]["awards_list"][0]["count"]:
                continue
            else:
                self.target = getattr(self, f"target_{num}-{i}")
                return True
        tkinter.messagebox.showinfo('提示', f"{num}等奖已抽完！")

    def set4(self, event):
        num = 4
        self.get_award_window(num)
        for i in range(len(env["awards_tuple"][num - 1]["awards_list"]) - 1, -1, -1):
            if getattr(self, f"target_{num}-{i}").size() >= env["awards_tuple"][num - 1]["awards_list"][0]["count"]:
                continue
            else:
                self.target = getattr(self, f"target_{num}-{i}")
                return True
        tkinter.messagebox.showinfo('提示', f"{num}等奖已抽完！")

    def set3(self, event):
        num = 3
        self.get_award_window(num)
        for i in range(len(env["awards_tuple"][num - 1]["awards_list"]) - 1, -1, -1):
            if getattr(self, f"target_{num}-{i}").size() >= env["awards_tuple"][num - 1]["awards_list"][0]["count"]:
                continue
            else:
                self.target = getattr(self, f"target_{num}-{i}")
                return True
        tkinter.messagebox.showinfo('提示', f"{num}等奖已抽完！")

    def set2(self, event):
        num = 2
        self.get_award_window(num)
        for i in range(len(env["awards_tuple"][num - 1]["awards_list"]) - 1, -1, -1):
            if getattr(self, f"target_{num}-{i}").size() >= env["awards_tuple"][num - 1]["awards_list"][0]["count"]:
                continue
            else:
                self.target = getattr(self, f"target_{num}-{i}")
                return True
        tkinter.messagebox.showinfo('提示', f"{num}等奖已抽完！")

    def set1(self, event):
        num = 1
        self.get_award_window(num)
        for i in range(len(env["awards_tuple"][num - 1]["awards_list"]) - 1, -1, -1):
            if getattr(self, f"target_{num}-{i}").size() >= env["awards_tuple"][num - 1]["awards_list"][0]["count"]:
                continue
            else:
                self.target = getattr(self, f"target_{num}-{i}")
                return True
        tkinter.messagebox.showinfo('提示', f"{num}等奖已抽完！")

    def close(self, event):
        self.root.withdraw()
        sys.exit()

    def get_award_window(self, num):
        prize_window = tkinter.Toplevel(self.root)
        prize_window.geometry('+{}+{}'
                              .format(int(self.screen_width*0.25), int(self.screen_height*0.25)))
        # 设置窗口标题
        prize_window.title("奖项内容")

        awards_list = env["awards_tuple"][num-1]["awards_list"]
        for i in range(len(awards_list)):
            prize_label = tkinter.Label(prize_window, text=awards_list[i]["name"], anchor="center")
            prize_label.grid(row=0, column=i, padx=10, pady=10)

            prize_image = Image.open(awards_list[i]["image"])\
                .resize((int(env["award_image_width"]), int(env["award_image_height"])))
            prize_image_tk = ImageTk.PhotoImage(prize_image)
            prize_image_label = tkinter.Label(prize_window, image=prize_image_tk, anchor="center")
            prize_image_label.image = prize_image_tk
            prize_image_label.grid(row=1, column=i, padx=10, pady=10)

            num_label = tkinter.Label(prize_window, text="抽选人数：{}".format(awards_list[i]["count"]), anchor="center")
            num_label.grid(row=2, column=i, padx=10, pady=10)


if __name__ == '__main__':
    data = pd.read_excel(env["list_people"])
    name_list = [item for item in data['姓名']]
    if len(name_list) >= get_awards_total(env["awards_tuple"]):
        c = LuckyDraw(name_list)
    else:
        raise Exception("Error: 人员数量小于配置的奖品总数！")
