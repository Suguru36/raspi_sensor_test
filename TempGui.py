#! /usr/bin/env python3
# coding: UTF-8
#ラベルの表示確認
#2019.01.16 by SGR

import tkinter
from sub.RaspiSensorTest import RaspiSensorTest
from sub.OneWireData import OneWireDataRead

import RPi.GPIO as GPIO


class TempGui(tkinter.Frame):
    """Top Level GUI"""
    def __init__(self, master=None):
        super().__init__(master, bg="skyblue",)
        self.pack()
        self.t=0
        self.h=0
        #RasberryPiデータ読み出しオブジェクト生成
        self.raspi_data1 = RaspiSensorTest()
        self.one_wire_temp = OneWireDataRead()
        #温湿度センサーの温度UI
        #温度センサー用のフレーム生成
        self.tmpHumOfTemp_Frame = tkinter.Frame(master=None)
        self.tmpHumOfTemp_Frame.pack(anchor=tkinter.W) #anchor=tkinter.W 左に寄せて
        #温度センサーお題目
        self.labelTemp1 = tkinter.Label(self.tmpHumOfTemp_Frame, text=u'温湿度センサー　温度:', bg='lightgray', relief=tkinter.FLAT)
        self.labelTemp1.pack(side=tkinter.LEFT) #左から詰める
        #温度表示部分
        self.tempVal1 = tkinter.Label(self.tmpHumOfTemp_Frame, text=u'xxxx', bg='yellow', relief=tkinter.FLAT)
        self.tempVal1.pack(side=tkinter.LEFT) #左から詰める
        #単位表示ラベル
        self.labelUnit1 = tkinter.Label(self.tmpHumOfTemp_Frame, text=u'℃', bg='lightgray', relief=tkinter.FLAT)
        self.labelUnit1.pack(side=tkinter.LEFT) #左から詰める

        #温湿度センサーの湿度
        #湿度表示用のフレーム
        self.tmpHumOfHum_Frame = tkinter.Frame(master)
        self.tmpHumOfHum_Frame.pack(anchor=tkinter.W) #tkinter.W 左に寄せて
        #湿度センサーのお題目
        self.labelHum = tkinter.Label(self.tmpHumOfHum_Frame, text=u'温湿度センサー　湿度:', bg='lightgray', relief=tkinter.FLAT)
        self.labelHum.pack(side=tkinter.LEFT) #左から詰める
        #湿度表示部分
        self.humVal1 = tkinter.Label(self.tmpHumOfHum_Frame, text=u'xxxx', bg='lightblue', relief=tkinter.FLAT)
        self.humVal1.pack(side=tkinter.LEFT) #左から詰める
        #湿度の単位
        self.labelUnit2 = tkinter.Label(self.tmpHumOfHum_Frame, text=u'%', bg='lightgray', relief=tkinter.FLAT)
        self.labelUnit2.pack(side=tkinter.TOP) #左から詰める


        #接触式温度センサー
        #湿度表示用のフレーム
        self.tmp_one_w_frame = tkinter.Frame(master)
        self.tmp_one_w_frame.pack(anchor=tkinter.W) #tkinter.W 左に寄せて
        #湿度センサーのお題目
        self.label_temp_one_w = tkinter.Label(self.tmp_one_w_frame, text=u'接触温度センサー　温度:', bg='lightgray', relief=tkinter.FLAT)
        self.label_temp_one_w.pack(side=tkinter.LEFT) #左から詰める
        #湿度表示部分
        self.tmp_Val2 = tkinter.Label(self.tmp_one_w_frame, text=u'xxxx', bg='pink', relief=tkinter.FLAT)
        self.tmp_Val2.pack(side=tkinter.LEFT) #左から詰める
        #湿度の単位
        self.labelUnit3 = tkinter.Label(self.tmp_one_w_frame, text=u'℃', bg='lightgray', relief=tkinter.FLAT)
        self.labelUnit3.pack(side=tkinter.TOP) #左から詰める

        self.update()

    #---温度の更新
    def update(self):
        self.t= self.one_wire_temp.read_temp()
        RaspiData=self.raspi_data1.get_data()
        self.tempVal1["text"] = "{:.2f}".format(RaspiData[0])

    #---湿度の更新
        self.humVal1["text"] = "{:.2f}".format(RaspiData[1])

    #---接触温度の更新
        self.tmp_Val2["text"] = "{:.2f}".format(self.t)

        self.after(1000, self.update)
            #この間に
        #
        #
        #必要なWidgetを記述する

###############################
if __name__ == '__main__':
    root = tkinter.Tk()
    app = TempGui(master=root)
    root.mainloop()
