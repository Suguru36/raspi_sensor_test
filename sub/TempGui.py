##! /usr/bin/env python
# coding: UTF-8
#ラベルの表示確認
#2019.01.16 by SGR

import tkinter

class TempGui(tkinter.Frame):
    def __init__(self, master=None):
        super().__init__(master, bg="skyblue",)
        self.pack()

        #温湿度センサーの温度UI
        #温度センサー用のフレーム生成
        self.tmpHueOfTemp_Frame = tkinter.Frame(master=None)
        self.tmpHueOfTemp_Frame.pack(anchor=tkinter.W) #anchor=tkinter.W 左に寄せて
        #温度センサーお題目
        self.labelTemp1 = tkinter.Label(self.tmpHueOfTemp_Frame, text=u'温湿度センサー　温度:', bg='lightgray', relief=tkinter.FLAT)
        self.labelTemp1.pack(side=tkinter.LEFT) #左から詰める
        #温度表示部分
        self.tempVal1 = tkinter.Label(self.tmpHueOfTemp_Frame, text=u'xxxx', bg='yellow', relief=tkinter.FLAT)
        self.tempVal1.pack(side=tkinter.LEFT) #左から詰める
        #単位表示ラベル
        self.labelUnit1 = tkinter.Label(self.tmpHueOfTemp_Frame, text=u'℃', bg='lightgray', relief=tkinter.FLAT)
        self.labelUnit1.pack(side=tkinter.LEFT) #左から詰める

        #温湿度センサーの湿度
        #湿度表示用のフレーム
        self.tmpHueOfHue_Frame = tkinter.Frame(master)
        self.tmpHueOfHue_Frame.pack(anchor=tkinter.W) #tkinter.W 左に寄せて
        #湿度センサーのお題目
        self.labelHue = tkinter.Label(self.tmpHueOfHue_Frame, text=u'温湿度センサー　湿度:', bg='lightgray', relief=tkinter.FLAT)
        self.labelHue.pack(side=tkinter.LEFT) #左から詰める
        #湿度表示部分
        self.hueVal1 = tkinter.Label(self.tmpHueOfHue_Frame, text=u'xxxx', bg='lightblue', relief=tkinter.FLAT)
        self.hueVal1.pack(side=tkinter.LEFT) #左から詰める
        #湿度の単位
        self.labelUnit2 = tkinter.Label(self.tmpHueOfHue_Frame, text=u'%', bg='lightgray', relief=tkinter.FLAT)
        self.labelUnit2.pack(side=tkinter.TOP) #左から詰める

    #---温度の更新
    def tempUpdate(self, temp):
        self.tempVal1["text"] = "{:.2f}".format(temp)

    #---湿度の更新
    def hueUpdate(self, hue):
        self.hueVal1["text"] = "{:.2f}".format(hue)
        #self.update
            #この間に
        #
        #
        #必要なWidgetを記述する

###############################
if __name__ == '__main__':
    root = tkinter.Tk()
    app = TempGui(master=root)
    app.tempUpdate(12.34)
    app.hueUpdate(43.21)
    root.mainloop()
