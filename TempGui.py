#! /usr/bin/env python3
# coding: UTF-8
#ラベルの表示確認
#2019.01.16 by SGR

import tkinter
import tkinter.simpledialog as sd
from sub.RaspiSensorTest import RaspiSensorTest
from sub.OneWireData import OneWireDataRead
import RPi.GPIO as GPIO


class TempGui(tkinter.Frame):
    
    """Top Level GUI"""
    def __init__(self, master=None):
        super().__init__(master, bg="skyblue",)
        self.pack()
        #RasberryPiデータ読み出しオブジェクト生成
        self.raspi_data1 = RaspiSensorTest()
        self.one_wire_temp = OneWireDataRead()

        #温湿度センサーの温度UI---------------------------------------------
        #温度センサー用のフレーム生成
        self.tmpHumOfTemp_Frame = tkinter.Frame(master, relief = tkinter.RIDGE ,bd = 5)
        self.tmpHumOfTemp_Frame.pack(anchor=tkinter.CENTER, padx=40) #anchor=tkinter.CENTER 中心に揃えて
        #温度センサーお題目
        self.labelTemp1 = tkinter.Label(self.tmpHumOfTemp_Frame, text=u'温湿度センサー　　温度:', bg='lightgray', relief=tkinter.FLAT)
        self.labelTemp1.pack(side=tkinter.LEFT) #左から詰める
        #温度表示部分
        self.tempVal1 = tkinter.Label(self.tmpHumOfTemp_Frame, text=u'xxxx', bg='yellow', relief=tkinter.FLAT)
        self.tempVal1.pack(side=tkinter.LEFT) #左から詰める
        #単位表示ラベル
        self.labelUnit1 = tkinter.Label(self.tmpHumOfTemp_Frame, text=u'℃', bg='lightgray', relief=tkinter.FLAT)
        self.labelUnit1.pack(side=tkinter.LEFT) #左から詰める

        #温湿度センサーの湿度---------------------------------------------
        #湿度表示用のフレーム
        self.tmpHumOfHum_Frame = tkinter.Frame(master, relief = tkinter.RIDGE ,bd = 5)
        self.tmpHumOfHum_Frame.pack(anchor=tkinter.CENTER, padx=40) #tkinter.CENTER 中心に揃えて
        #湿度センサーのお題目
        self.labelHum = tkinter.Label(self.tmpHumOfHum_Frame, text=u'温湿度センサー　　湿度:', bg='lightgray', relief=tkinter.FLAT)
        self.labelHum.pack(side=tkinter.LEFT) #左から詰める
        #湿度表示部分
        self.humVal1 = tkinter.Label(self.tmpHumOfHum_Frame, text=u'xxxx', bg='lightblue', relief=tkinter.FLAT)
        self.humVal1.pack(side=tkinter.LEFT) #左から詰める
        #湿度の単位
        self.labelUnit2 = tkinter.Label(self.tmpHumOfHum_Frame, text=u'%', bg='lightgray', relief=tkinter.FLAT)
        self.labelUnit2.pack(side=tkinter.TOP) #左から詰める

        #接触式温度センサー ---------------------------------------------
        #湿度表示用のフレーム
        self.tmp_one_w_frame = tkinter.Frame(master, relief = tkinter.RIDGE ,bd = 5)
        self.tmp_one_w_frame.pack(anchor=tkinter.CENTER, padx=40) #tkinter.CENTER 中心に揃えて
        #湿度センサーのお題目
        self.label_temp_one_w = tkinter.Label(self.tmp_one_w_frame, text=u'接触温度センサー　温度:', bg='lightgray', relief=tkinter.FLAT)
        self.label_temp_one_w.pack(side=tkinter.LEFT) #左から詰める
        #湿度表示部分
        self.tmp_Val2 = tkinter.Label(self.tmp_one_w_frame, text=u'xxxx', bg='pink', relief=tkinter.FLAT)
        self.tmp_Val2.pack(side=tkinter.LEFT) #左から詰める
        #湿度の単位
        self.labelUnit3 = tkinter.Label(self.tmp_one_w_frame, text=u'℃', bg='lightgray', relief=tkinter.FLAT)
        self.labelUnit3.pack(side=tkinter.TOP) #左から詰める

        #温度設定Control -----------------------------------------
        #フレーム
        self.tmp_target_frame = tkinter.Frame(master, relief = tkinter.RIDGE ,bd = 5)
        self.tmp_target_frame.pack(anchor=tkinter.E, fill=tkinter.X, padx=40) #tkinter. 中心に揃えて
        #お題目
        self.label_temp_set = tkinter.Label(self.tmp_target_frame, text=u'設定温度 ', bg='lightgray', relief=tkinter.FLAT)
        self.label_temp_set.pack(side=tkinter.LEFT) #左から詰める
        #単位
        self.label_temp_set_unit = tkinter.Label(self.tmp_target_frame, text=u' ℃', bg='lightgray', relief=tkinter.FLAT)
        self.label_temp_set_unit.pack(side=tkinter.RIGHT) #左から詰める
        #表示部分
        self.tmp_target = tkinter.Label(self.tmp_target_frame,  text=u'45.0 ', bg='white', relief=tkinter.FLAT)
        self.tmp_target.pack(side=tkinter.RIGHT) #左から詰める
        #設定ボタン
        self.temp_set_button = tkinter.Button(self.tmp_target_frame, text="Set", command = self.temp_set)
        self.temp_set_button.pack(side=tkinter.RIGHT) #左から詰める

        #温度制御ファンインジゲータ -----------------------------------------
        #温度制御は　：　GPIO17Lo出力（の予定）
        #フレーム
        self.tmp_control_fan = tkinter.Frame(master, relief = tkinter.RIDGE ,bd = 5)
        self.tmp_control_fan.pack(anchor=tkinter.E, fill=tkinter.X, padx=40) #tkinter. 中心に揃えて
        #お題目
        self.label_temp_fan = tkinter.Label(self.tmp_control_fan, text=u'冷却ファン ', bg='lightgray', relief=tkinter.FLAT)
        self.label_temp_fan.pack(side=tkinter.LEFT) #左から詰める
        #表示部分
        self.label_on_off = tkinter.Label(self.tmp_control_fan, text=u'OFF ', bg='green', relief=tkinter.SUNKEN ,bd = 5)
        self.label_on_off.pack(side=tkinter.RIGHT) #左から詰める

        self.update()

    #---温度の更新
    def update(self):

        self.RaspiData = self.raspi_data1.get_data()
        self.tempVal1["text"] = "{:.2f}".format(self.RaspiData[0])
        #---湿度の更新
        self.humVal1["text"] = "{:.2f}".format(self.RaspiData[1])
        #---接触温度の更新
        self.wire_temp_sens = self.one_wire_temp.read_temp()
        self.tmp_Val2["text"] = "{:.2f}".format(self.wire_temp_sens)
        #---温度を監視するルーチンをここに
        if self.wire_temp_sens > float(self.tmp_target["text"]):
            #設定温度より高いときの制御をここへ
            self.label_on_off["text"] = "ON"
            self.label_on_off["bg"] = "red"
            self.label_on_off.relief=tkinter.RAISED
        else:
            #設定温度よりも低いときの制御をここへ
            self.label_on_off["text"] = "OFF"
            self.label_on_off["bg"] = "green"
            self.label_on_off.relief=tkinter.SUNKEN
        #--------------------------

        self.after(1000, self.update)
        #この間に

    def temp_set(self):
        """temp_set_button押下時に設定温度を入力するファンクション"""
        self.tmp_target["text"] = "{:.1f}".format(sd.askinteger("設定温度", "設定温度を入力"))


###############################
if __name__ == '__main__':
    root = tkinter.Tk()
    root.title("温度湿度測定") #Windowタイトル設定
#    root.geometry("300x200")  #Windowサイズ設定
    app = TempGui(master=root)
    root.mainloop()
