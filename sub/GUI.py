#! /usr/bin/env python
# coding: UTF-8
#ラベルの表示確認
#2019.01.16 by SGR

import tkinter

class MyGui(tkinter.Frame):
    def __init__(self, master=None):
        super().__init__(master, bg="skyblue",)
        self.pack()
        
        #この間に
        #
        #
        #必要なWidgetを記述する
        
###############################
if __name__ == '__main__':
    root = tkinter.Tk()
    app = MyGui(master=root)
    root.mainloop()