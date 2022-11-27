#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author:yimi

import copy
import sqlite3
import tkinter as tk  # 使用Tkinter前需要先导入

# 实例化object，建立窗口window
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename

window = tk.Tk()

frame = tk.Frame(window, relief=SUNKEN, borderwidth=2, width=450, height=250)
frame.pack(side=TOP, fill=BOTH, expand=1)
# 设置窗口大小
winWidth = 600
winHeight = 400
# 获取屏幕分辨率
screenWidth = window.winfo_screenwidth()
screenHeight = window.winfo_screenheight()

x = int((screenWidth - winWidth) / 2)
y = int((screenHeight - winHeight) / 2)

# 给窗口的可视化起名字
window.title('PyDbAdmin')
# 设置窗口初始位置在屏幕居中
window.geometry("%sx%s+%s+%s" % (winWidth, winHeight, x, y))

listbox1 = tk.Listbox(frame, highlightthickness=0)

# 定义列

tree_date = ttk.Treeview(frame, show='headings')


def do_job():
    print(1)


def select_file():
    filepath = askopenfilename(title='Please choose a file', initialdir='./', filetypes=[('Sqlite file', '*.db')])
    sql_open(filepath)

c = 1

def sql_open(path):
    global c
    if c != 1:
        c.close()
        listbox1.delete(0, END)
    c = sqlite3.connect(path)
    c.cursor()
    cursor = c.execute("SELECT * FROM sqlite_master WHERE type ='table'")
    listbox1.place(relx=0.01, rely=0.01, relwidth=0.49, relheight=0.98)
    for row in cursor:
        listbox1.insert("end", row[1])
    listbox1.bind('<<ListboxSelect>>', listbox_click)
    # conn.close()


def table_init(column, data):
    tree_date['columns'] = column
    tree_date.place(relx=0.5, rely=0.01, relwidth=0.49, relheight=0.98)

    # # 设置列宽度
    for i in column:
        tree_date.column(i, width=50)

    # 添加列名
    for i in column:
        tree_date.heading(i, text=i)

    index = 0
    for i in data:
        tree_date.insert('', index, values=i)
        index = index + 1


def listbox_click(even):
    # 向文本区光标处插入列表框当前选中文本
    table = listbox1.get(listbox1.curselection())
    cursor = c.execute("pragma table_info('" + table + "')")
    head = []
    for row in cursor:
        head.append(row[1])
    cursor = c.execute("SELECT * from " + table)
    table_init(head, cursor)


# 创建一个菜单栏，这里我们可以把他理解成一个容器，在窗口的上方
menubar = tk.Menu(window)

# 创建一个File菜单项（默认不下拉，下拉内容包括New，Open，Save，Exit功能项）
filemenu = tk.Menu(menubar, tearoff=0)
# 将上面定义的空菜单命名为File，放在菜单栏中，就是装入那个容器中
menubar.add_cascade(label='菜单', menu=filemenu)

# 在File中加入New、Open、Save等小菜单，即我们平时看到的下拉菜单，每一个小菜单对应命令操作。
filemenu.add_command(label='选择', command=select_file)

# filemenu.add_separator()  # 添加一条分隔线
filemenu.add_command(label='退出', command=window.quit)  # 用tkinter里面自带的quit()函数

# 创建菜单栏完成后，配置让菜单栏menubar显示出来
window.config(menu=menubar)

# 主窗口循环显示
window.mainloop()
