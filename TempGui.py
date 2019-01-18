##! /usr/bin/env python
# coding: UTF-8
#ラベルの表示確認
#2019.01.16 by SGR

import tkinter
import RaspiSensorTest as RaspiSensorTest
import RPi.GPIO as GPIO

class TempGui(tkinter.Frame):
    def __init__(self, master=None):
        super().__init__(master, bg="skyblue",)
        self.pack()
        #RasberryPiデータ読み出しオブジェクト生成
#        RaspiSensor = RaspiSensorTest()

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

        self.update()

    #---温度の更新
    def  update(self):
#        RaspiData = RaspiSensor.getData()
        RaspiData[2, 4]
        self.tempVal1["text"] = "{:.2f}".format(RaspiData[0])

    #---湿度の更新
        self.humVal1["text"] = "{:.2f}".format(RaspiData[1])
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
