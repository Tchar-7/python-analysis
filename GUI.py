import tkinter as tk
from tkinter import StringVar, ttk
import openpyxl


class stone:
    def __init__(self, r, name1, lv1, name2, lv2, hole):
        self.rarity = r
        self.name1 = name1
        if self.name1 == "无":
            self.lv1 = '0'
        else:
            self.lv1 = lv1
        self.name2 = name2
        if self.name2 == "无":
            self.lv2 = '0'
        else:
            self.lv2 = lv2
        self.hole = hole

    def judge(self):
        return 0


class MH_GUI:
    def __init__(self):
        self.top = tk.Tk()
        self.top.geometry("500x300")
        self.top.resizable(0, 0)
        self.top.title("Monster Hunter Stone")
        self.name_list = []
        self.hole_list = []
        self.rarit_list = []
        self.read_name_list('.\skill.xlsx', '.\stone.xlsx')
        self.r_list = ['0', '1', '2', '3']
        self.init_combobox()
        self.init_lables()
        self.init_button()
        self.top.mainloop()

    def init_button(self):
        self.button = tk.Button(self.top, text="评判", command=lambda: self.action()).place(x=240, y=250)

    def action(self):
        TheStone = stone(self.value6.get(), self.value1.get(), self.value2.get(), self.value3.get(), self.value4.get(), self.value5.get())
        TheStone.judge()

    def init_lables(self):
        self.label1 = tk.Label(self.top, text="技能1:").place(x=150, y=10)
        self.label2 = tk.Label(self.top, text="Lv:").place(x=150, y=50)
        self.label3 = tk.Label(self.top, text="技能2:").place(x=150, y=90)
        self.label4 = tk.Label(self.top, text="Lv:").place(x=150, y=130)
        self.label5 = tk.Label(self.top, text="孔位").place(x=150, y=170)
        self.label5 = tk.Label(self.top, text="稀有度").place(x=150, y=210)

    def init_combobox(self):
        self.value1 = StringVar()
        self.value1.set("请选择技能1")
        self.value2 = StringVar()
        self.value2.set("选择其等级")
        self.value3 = StringVar()
        self.value3.set("请选择技能2")
        self.value4 = StringVar()
        self.value4.set("选择其等级")
        self.value5 = StringVar()
        self.value5.set("请选择其孔位")
        self.value6 = StringVar()
        self.value6.set("请选择其稀有度")
        self.combobox1 = ttk.Combobox(self.top, textvariable=self.value1, height=10, width=20, values=self.name_list).place(x=200, y=10)
        self.combobox2 = ttk.Combobox(self.top, textvariable=self.value2, height=len(self.r_list), width=20, values=self.r_list).place(x=200, y=50)
        self.combobox3 = ttk.Combobox(self.top, textvariable=self.value3, height=10, width=20, values=self.name_list).place(x=200, y=90)
        self.combobox4 = ttk.Combobox(self.top, textvariable=self.value4, height=len(self.r_list), width=20, values=self.r_list).place(x=200, y=130)
        self.combobox5 = ttk.Combobox(self.top, textvariable=self.value5, height=10, width=20, values=self.hole_list).place(x=200, y=170)
        self.combobox6 = ttk.Combobox(self.top, textvariable=self.value6, height=10, width=20, values=self.rarit_list).place(x=200, y=210)

    def read_name_list(self, data_res, data_res1):
        readbook = openpyxl.load_workbook(data_res)
        sheet = readbook['skill']    # 名字的方式
        rows = sheet.max_row  # 行
        for i in range(2, rows+1):
            data = sheet.cell(i, 1).value
            self.name_list.append(data)
        readbook = openpyxl.load_workbook(data_res1)
        sheet = readbook['マカ錬金 幽玄 -ZH']    # 名字的方式
        rows = sheet.max_row  # 行
        for i in range(2, rows+1):
            data = sheet.cell(i, 6).value
            self.hole_list.append(data)
        self.hole_list = list(set(self.hole_list))
        readbook = openpyxl.load_workbook(data_res1)
        sheet = readbook['マカ錬金 幽玄 -ZH']    # 名字的方式
        rows = sheet.max_row  # 行
        for i in range(2, rows+1):
            data = sheet.cell(i, 1).value
            self.rarit_list.append(data)
        self.rarit_list = list(set(self.rarit_list))


mh = MH_GUI()