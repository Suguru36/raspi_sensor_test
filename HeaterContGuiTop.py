#! /usr/bin/env python3
# coding: UTF-8
#ラベルの表示確認
#2019.01.16 by SGR

import tkinter
import tkinter.simpledialog as sd
from tkinter import messagebox
from sub.GetAruduinoDataHeatCont import GetAruduinoDataHeatCnt
import RPi.GPIO as GPIO
import time
from sub.SpiRW import SpiRW
import csv
#import pandas

#---------------------------------------------------------





class TempGui(tkinter.Frame):
   #--------- Data Cluster --------
    arduino_param_0 = {'ir_temp' : 0 , 'ambient_temp' : 0 ,'distance' : 0 , 'target_temp' : 50 , 'distance_limit' : 300, 'heatter_condition' : False}
    arduino_param_1 = {'ir_temp' : 0 , 'ambient_temp' : 0 ,'distance' : 0 , 'target_temp' : 50 , 'distance_limit' : 300, 'heatter_condition' : False}
    arduino_param_2 = {'ir_temp' : 0 , 'ambient_temp' : 0 ,'distance' : 0 , 'target_temp' : 50 , 'distance_limit' : 300, 'heatter_condition' : False}


    """Top Level GUI"""
    def __init__(self, master=None):
        #-----------------------------------------------------------------------------
        class UserControler(object):
            """ユーザー用コントロールボックスオブジェクト"""
            #----------------------------------------------
            def __init__(self):
                #GPIOのPin指定モードをBCMへ設定
                GPIO.setmode(GPIO.BCM)
                #------  使用するピンの入出力宣言
                #出力ピン
                GPIO.setup(22, GPIO.OUT) #GPIO22 出力 CNT0
                GPIO.setup(23, GPIO.OUT) #GPIO23 出力 CNT1
                GPIO.setup(24, GPIO.OUT) #GPIO24 出力 CNT2
                #入力ピン
                GPIO.setup(25, GPIO.IN, pull_up_down = GPIO.PUD_UP) #GPIO25 入力　SW Pullup
                GPIO.setup(26, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) #GPIO26 入力　EMO Pulldown
                #出力ピンの初期値設定
                GPIO.output(22, 0)      #Lo出力
                GPIO.output(23, 0)      #Lo出力
                GPIO.output(24, 0)      #Lo出力0

            #----------------------------------------------
            def set_led_mode(self, cnt2 ,cnt1 ,cnt0):
                """000:スタンバイ ,001青, 010緑, 011加熱中表示, 100加熱保温中, 101加熱完了呼び出し"""
                #出力ピンの初期値設定
                GPIO.output(22, cnt0)      #Lo出力
                GPIO.output(23, cnt1)      #Lo出力
                GPIO.output(24, cnt2)      #Lo出力

        #-----------------------------------------------------------------------------
        class SensorDataUiFrame(object):
            """各センサーのデータを表示する最小のフレームクラス"""
            def __init__(self, target_frame, label_name, unit, label_color, flame_color, default_value):
                """引数はすべて文字列"""
                #温度センサー用のフレーム生成\
                self.Uiframe = tkinter.Frame(target_frame, relief = tkinter.RIDGE ,bd = 5)
                self.Uiframe.pack(fill = tkinter.X, anchor=tkinter.CENTER, padx=10) #anchor=tkinter.CENTER 中心に揃えて
                #温度センサーお題目
                self.label_param_name = tkinter.Label(self.Uiframe, text = label_name, bg = flame_color, relief=tkinter.FLAT)
                self.label_param_name.pack( anchor=tkinter.W, side = tkinter.LEFT) #左から詰める
                #単位表示ラベル
                self.labelUnit = tkinter.Label(self.Uiframe, text = unit, bg = flame_color, relief=tkinter.FLAT)
                self.labelUnit.pack(anchor=tkinter.E, side=tkinter.RIGHT) #左から詰める
                #温度表示部分
                self.label_value = tkinter.Label(self.Uiframe, text = default_value, bg = label_color, relief=tkinter.FLAT)
                self.label_value.pack(anchor=tkinter.E, side=tkinter.RIGHT) #左から詰める

            def change_value(self, value):
                """表示データ変更用メソッド"""
                self.label_value["text"] = "{:.2f}".format(value)

            def change_distance(self, value):
                """表示データ変更用メソッド"""
                self.label_value["text"] = "{:d}".format(value)
        #-----------------------------------------------------------------------------
        class TempControlTargetFrame(object):
            """温度設定UIのフレームクラス"""
            def __init__(self, target_frame, name , button_name, default_value, unit):
                #フレーム
                self.tmp_target_frame = tkinter.Frame(target_frame, relief = tkinter.RIDGE ,bd = 5)
                self.tmp_target_frame.pack(fill = tkinter.X, anchor=tkinter.CENTER, padx=10) #tkinter. 中心に揃えて
                #お題目
                self.label_temp_set = tkinter.Label(self.tmp_target_frame, text = name , bg='lightgray', relief=tkinter.FLAT)
                self.label_temp_set.pack(side=tkinter.LEFT) #左から詰める
                #単位
                self.label_temp_set_unit = tkinter.Label(self.tmp_target_frame, text = unit, bg='lightgray', relief=tkinter.FLAT)
                self.label_temp_set_unit.pack(side=tkinter.RIGHT) #左から詰める
                #表示部分
                self.tmp_target = tkinter.Label(self.tmp_target_frame,  text = default_value, bg='white', relief=tkinter.FLAT)
                self.tmp_target.pack(side=tkinter.RIGHT) #左から詰める

                #設定ボタン 温度設定キーボード版
#                self.temp_set_button = tkinter.Button(self.tmp_target_frame, text = button_name, command = self.set_target_temp)
#                self.temp_set_button.pack(side=tkinter.RIGHT) #左から詰める

                #温度設定＋＆ーボタン版
                #プラス
                self.temp_set_button_P = tkinter.Button(self.tmp_target_frame, text = "+", command = self.set_target_temp_p)
                self.temp_set_button_P.pack(side=tkinter.RIGHT) #左から詰める
                #マイナス
                self.temp_set_button_M = tkinter.Button(self.tmp_target_frame, text = "-", command = self.set_target_temp_m)
                self.temp_set_button_M.pack(side=tkinter.RIGHT) #左から詰める


            def get_target_value(self):
                """設定温度取得メソッド"""
                return int(self.tmp_target["text"])
            def set_target_value(self, value):
                """表示データ変更用メソッド"""
                self.tmp_target["text"] = "{:d}".format(value)
            def set_target_temp(self):
                """temp_set_button押下時に設定温度を入力するファンクション"""
                self.tmp_target["text"] = "{:d}".format(sd.askinteger("設定温度", "設定温度を入力"))
            def set_target_temp_p(self):
                """設定温度をインクリメントする"""
                self.tmp_target["text"] = int(self.tmp_target["text"]) + 1
            def set_target_temp_m(self):
                """設定温度をディクリメントする"""
                self.tmp_target["text"] = int(self.tmp_target["text"]) - 1


        #-----------------------------------------------------------------------------
        class HeaterIndicatorFrame(object):
            """ヒーターの状態表示フレームクラス"""
            def __init__(self, target_frame, name ,master = None):
                #温度制御ファンインジゲータ -----------------------------------------
                #温度制御は　：　GPIO17Lo出力（の予定）
                #フレーム
                self.tmp_control_fan = tkinter.Frame(target_frame, relief = tkinter.RIDGE ,bd = 5)
                self.tmp_control_fan.pack(fill = tkinter.X, anchor=tkinter.E, padx=10) #tkinter. 中心に揃えて
                #お題目
                self.label_temp_fan = tkinter.Label(self.tmp_control_fan, text= name , bg='lightgray', relief=tkinter.FLAT)
                self.label_temp_fan.pack(side=tkinter.LEFT) #左から詰める
                #表示部分
                self.label_on_off = tkinter.Label(self.tmp_control_fan, text=u'OFF ', bg='green', relief=tkinter.SUNKEN ,bd = 5)
                self.label_on_off.pack(side=tkinter.RIGHT) #左から詰める
            def set_state_ON(self):
                #外部スイッチのＵＩ「ＯＮ」表示
                self.label_on_off["text"] = "ON"
                self.label_on_off["bg"] = "red"
                self.label_on_off.relief=tkinter.RAISED
            def set_state_OFF(self):
                #外部スイッチのＵＩ「ＯＦＦ」表示
                self.label_on_off["text"] = "OFF"
                self.label_on_off["bg"] = "green"
                self.label_on_off.relief=tkinter.SUNKEN
        #-----------------------------------------------------------------------------
        class ArduinoDataFrame(object):
            """Arduino単位のUIを発生させるクラス（3個分）"""
            def __init__(self):
                #Arduino単位のフレームを生成
                arduino0_fraeme = tkinter.Frame(master = None, relief = tkinter.RIDGE ,bd = 5)
                arduino0_fraeme.pack(anchor=tkinter.CENTER, side = tkinter.LEFT, padx=10) #anchor=tkinter.CENTER 中心に揃えて
                #メインフレームのタイトル
                self.TempCntLabel_0 = tkinter.Label(arduino0_fraeme, text= 'Temp Control 1' , bg='lightgray', relief=tkinter.FLAT)
                self.TempCntLabel_0.pack(side=tkinter.TOP, anchor=tkinter.W) #左から詰める
                #各センサーのＵＩ生成
                self.ir_temp0     = SensorDataUiFrame(arduino0_fraeme, "ワーク表面温度", "℃", "Yellow", "lightgray", "00000")
                self.amb_temp0    = SensorDataUiFrame(arduino0_fraeme, "周辺温度", "℃", "skyblue", "lightgray", "00000")
                self.distance0    = SensorDataUiFrame(arduino0_fraeme, "測距センサー", "mm", "pink", "lightgray", "00000")
                self.cnt_target0   = TempControlTargetFrame(arduino0_fraeme, "設定温度", "Set", "55", "℃")
                self.heater_state0 = HeaterIndicatorFrame(arduino0_fraeme, "ヒーター(未完成)")

                #Arduino単位のフレームを生成
                arduino1_fraeme = tkinter.Frame(master = None, relief = tkinter.RIDGE ,bd = 5)
                arduino1_fraeme.pack(anchor=tkinter.CENTER, side = tkinter.LEFT, padx=20) #anchor=tkinter.CENTER 中心に揃えて
                #メインフレームのタイトル
                self.TempCntLabel_1 = tkinter.Label(arduino1_fraeme, text= 'Temp Control 2' , bg='lightgray', relief=tkinter.FLAT)
                self.TempCntLabel_1.pack(side=tkinter.TOP, anchor=tkinter.W) #左から詰める
                #各センサーのＵＩ生成                self.ir_temp     = SensorDataUiFrame(arduino1_fraeme, "ワーク表面温度", "UNIT", "Yellow", "lightgray", "00000")
                self.ir_temp1     = SensorDataUiFrame(arduino1_fraeme, "ワーク表面温度", "℃", "Yellow", "lightgray", "00000")
                self.amb_temp1    = SensorDataUiFrame(arduino1_fraeme, "周辺温度", "℃", "skyblue", "lightgray", "00000")
                self.distance1    = SensorDataUiFrame(arduino1_fraeme, "測距センサー", "mm", "pink", "lightgray", "00000")
                self.cnt_target1   = TempControlTargetFrame(arduino1_fraeme, "設定温度", "Set", "55", "℃")
                self.heater_state1 = HeaterIndicatorFrame(arduino1_fraeme, "ヒーター(未完成)")

                #Arduino単位のフレームを生成
                arduino2_fraeme = tkinter.Frame(master = None, relief = tkinter.RIDGE ,bd = 5)
                arduino2_fraeme.pack(anchor=tkinter.CENTER, side = tkinter.LEFT, padx=20) #anchor=tkinter.CENTER 中心に揃えて
                #メインフレームのタイトル
                self.TempCntLabel_2 = tkinter.Label(arduino2_fraeme, text= 'Temp Control 3' , bg='lightgray', relief=tkinter.FLAT)
                self.TempCntLabel_2.pack(side=tkinter.TOP, anchor=tkinter.W) #左から詰める
                #各センサーのＵＩ生成                self.ir_temp     = SensorDataUiFrame(arduino1_fraeme, "ワーク表面温度", "UNIT", "Yellow", "lightgray", "00000")
                self.ir_temp2     = SensorDataUiFrame(arduino2_fraeme, "ワーク表面温度", "℃", "Yellow", "lightgray", "00000")
                self.amb_temp2    = SensorDataUiFrame(arduino2_fraeme, "周辺温度", "℃", "skyblue", "lightgray", "00000")
                self.distance2    = SensorDataUiFrame(arduino2_fraeme, "測距センサー", "mm", "pink", "lightgray", "00000")
                self.cnt_target2   = TempControlTargetFrame(arduino2_fraeme, "設定温度", "Set", "55", "℃")
                self.heater_state2 = HeaterIndicatorFrame(arduino2_fraeme, "ヒーター(未完成)")
#----------------------------------------------------
#-------まだTopLevelClassの__init__は続くよ
        self.num = 0

        super().__init__(master, bg="skyblue",)
        self.pack()
        #設定ファイルから初期設定地を取得してクラス変数に格納する
        with open("/home/pi/dev/raspi_sensor_test/HeatCont.ini" , 'r' ) as self.FileIni:
            #ファイルの内容取得
            self.read_csv = csv.reader( self.FileIni, delimiter = '\t')
             #１行目のヘッダを無視する
            next(self.read_csv)
            #設定ファイルの内容をクラス変数に格納する
            self.arduino_param_0['target_temp']    = int((next(self.read_csv))[1]) #１行目のデータを格納
            self.arduino_param_0['distance_limit'] = int((next(self.read_csv))[1]) #２行目のデータを格納
            self.arduino_param_1['target_temp']    = int((next(self.read_csv))[1]) #３行目のデータを格納
            self.arduino_param_1['distance_limit'] = int((next(self.read_csv))[1]) #４行目のデータを格納
            self.arduino_param_2['target_temp']    = int((next(self.read_csv))[1]) #３行目のデータを格納
            self.arduino_param_2['distance_limit'] = int((next(self.read_csv))[1]) #４行目のデータを格納

        #RasberryPiデータ読み出しオブジェクト生成
        self.ardu0 = GetAruduinoDataHeatCnt(8,0) # 8Byte単位でデバイス0番
        self.ardu1 = GetAruduinoDataHeatCnt(8,1) # 8Byte単位でデバイス1番
        self.ardu2 = GetAruduinoDataHeatCnt(8,2) # 8Byte単位でデバイス2番
        self.main_ui = ArduinoDataFrame()        #メインＵＩ生成
        self.usr_cnt = UserControler()           #ユーザーコントロールボックスオブジェクト
        self.usr_cnt.set_led_mode(0,0,0)         #コントロールボックスのLEDを初期化


        #クラス変数(UIの値)初期値設定
        self.arduino_param_0['ir_temp'] = 999.99   #温度設定
        self.arduino_param_0['ambient_temp'] = 999.99
        self.arduino_param_0['distance'] =9999
        self.arduino_param_0['heatter_condition'] = False

        self.main_ui.ir_temp0.change_value(self.arduino_param_0['ir_temp'])
        self.main_ui.amb_temp0.change_value(self.arduino_param_0['ambient_temp'])
        self.main_ui.distance0.change_distance(self.arduino_param_0['distance'])
        self.main_ui.cnt_target0.set_target_value(self.arduino_param_0['target_temp'])

        self.arduino_param_1['ir_temp'] = 999.99   #温度設定
        self.arduino_param_1['ambient_temp'] = 999.99
        self.arduino_param_1['distance'] =9999
        self.arduino_param_1['heatter_condition'] = False
        self.main_ui.ir_temp1.change_value(self.arduino_param_1['ir_temp'])
        self.main_ui.amb_temp1.change_value(self.arduino_param_1['ambient_temp'])
        self.main_ui.distance1.change_distance(self.arduino_param_1['distance'])
        self.main_ui.cnt_target1.set_target_value(self.arduino_param_1['target_temp'])


        self.arduino_param_2['ir_temp'] = 999.99   #温度設定
        self.arduino_param_2['ambient_temp'] = 999.99
        self.arduino_param_2['distance'] =9999
        self.arduino_param_2['heatter_condition'] = False
        self.main_ui.ir_temp2.change_value(self.arduino_param_2['ir_temp'])
        self.main_ui.amb_temp2.change_value(self.arduino_param_2['ambient_temp'])
        self.main_ui.distance2.change_distance(self.arduino_param_2['distance'])
        self.main_ui.cnt_target2.set_target_value(self.arduino_param_2['target_temp'])

        self.update()

    #---温度の更新

    def update(self):
        """100ms/１回の更新頻度"""
        #Arduino0のデータ取得
        self.arduino0_data = self.ardu0.GetDataArd()
        #放射温度
        self.arduino_param_0['ir_temp'] = (self.arduino0_data)[0]   #温度設定
        self.main_ui.ir_temp0.change_value(self.arduino_param_0['ir_temp'])
        #周辺温度
        self.arduino_param_0['ambient_temp'] = (self.arduino0_data)[1]   #温度設定
        self.main_ui.amb_temp0.change_value(self.arduino_param_0['ambient_temp'])
        #レーザー測距計
        self.arduino_param_0['distance'] = (self.arduino0_data)[2]   #温度設定
        self.main_ui.distance0.change_distance(self.arduino_param_0['distance'])
        #UIの設定温度取得
        self.arduino_param_0['target_temp'] = self.main_ui.cnt_target0.get_target_value()
        self.ardu0.SetTempTarget(self.arduino_param_0['target_temp'])

        #-----------------------------
        #Arduino1のデータ取得
        self.arduino1_data = self.ardu1.GetDataArd()
        #放射温度
        self.arduino_param_1['ir_temp'] = (self.arduino1_data)[0]   #温度設定
        self.main_ui.ir_temp1.change_value(self.arduino_param_1['ir_temp'])
        #周辺温度
        self.arduino_param_1['ambient_temp'] = (self.arduino1_data)[1]   #温度設定
        self.main_ui.amb_temp1.change_value(self.arduino_param_1['ambient_temp'])
        #レーザー測距計
        self.arduino_param_1['distance'] = (self.arduino1_data)[2]   #温度設定
        self.main_ui.distance1.change_distance(self.arduino_param_1['distance'])
        #UIの設定温度取得
        self.arduino_param_1['target_temp'] = self.main_ui.cnt_target1.get_target_value()
        self.ardu1.SetTempTarget(self.arduino_param_1['target_temp'])

        #-----------------------------
        #Arduino2のデータ取得
        self.arduino2_data = self.ardu2.GetDataArd()
        #放射温度
        self.arduino_param_2['ir_temp'] = (self.arduino2_data)[0]   #温度設定
        self.main_ui.ir_temp2.change_value(self.arduino_param_2['ir_temp'])
        #周辺温度
        self.arduino_param_2['ambient_temp'] = (self.arduino2_data)[1]   #温度設定
        self.main_ui.amb_temp2.change_value(self.arduino_param_2['ambient_temp'])
        #レーザー測距計
        self.arduino_param_2['distance'] = (self.arduino2_data)[2]   #温度設定
        self.main_ui.distance2.change_distance(self.arduino_param_2['distance'])
        #UIの設定温度取得
        self.arduino_param_2['target_temp'] = self.main_ui.cnt_target2.get_target_value()
        self.ardu2.SetTempTarget(self.arduino_param_2['target_temp'])

        #---温度＋距離＋EMO,WSを監視するルーチンをここに追記する！！！




#        if 10 > float(self.tmp_target["text"]):
            #設定温度より高いときの制御をここへ
#            self.main_ui.heater_state0.set_state_ON()
#        else:
            #設定温度よりも低いときの制御をここへ
#            self.main_ui.heater_state0.set_state_OFF()




        #--------------------------
        self.after(1, self.update) #1ms毎に実行する
        #この間に


###############################
if __name__ == '__main__':
    root = tkinter.Tk()
    root.title("温度湿度測定") #Windowタイトル設定
#    root.geometry("300x200")  #Windowサイズ設定
    app = TempGui(master=root)

#----- GUI が閉じられたら本当に閉じるのか？とポップアップメニュー
    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
#------------------------------------------
#- プログラム停止後の初期化処理
    #GPIOの初期化
    GPIO.cleanup()
#----------------------------------

    root.mainloop()
