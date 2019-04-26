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
from sub.YaniStateMachine import StateMachine
import csv
#import pandas

#---------------------------------------------------------





class TempGui(tkinter.Frame):
   #--------- Data Cluster --------
    arduino_param_0 = {'ir_temp' : 999 , 'ambient_temp' : 999 ,'distance' : 9999 , 'target_temp' : 50 , 'distance_limit' : 300, 'heater_condition' : False, 'heater_enable' : False, 'temp_reach' : False, 'work_det' : False}
    arduino_param_1 = {'ir_temp' : 999 , 'ambient_temp' : 999 ,'distance' : 9999 , 'target_temp' : 50 , 'distance_limit' : 300, 'heater_condition' : False, 'heater_enable' : False, 'temp_reach' : False, 'work_det' : False}
    arduino_param_2 = {'ir_temp' : 999 , 'ambient_temp' : 999 ,'distance' : 9999 , 'target_temp' : 50 , 'distance_limit' : 300, 'heater_condition' : False, 'heater_enable' : False, 'temp_reach' : False, 'work_det' : False}

    PROXIMILITTY_LIMIT = 30 #近接判定距離定数

    #-------- class 定数の定義 GPIOのPin番号定義(BCM)
    _CNT0 = 22         #CNT0 コントロールBit0
    _CNT1 = 23         #CNT2 コントロールBit1
    _CNT2 = 24         #CNT2 コントロールBit2

    _SW_FN  = 25       #ファンクションスイッチのGPIO
    _EMO_SW = 26       #EMOスイッチのGPIO


    """Top Level GUI"""
    def __init__(self, master=None):
        #-----------------------------------------------------------------------------
        class UserControler(object):
            """ユーザー用コントロールボックスオブジェクト"""
            #----------------------------------------------
            def __init__(self):
                self.sw_previous_state = 1      #前回のツイッチの状況保持関数
                self.naga_oshi_kenshutu = 0     #長押しのカウンター変数初期化

                #GPIOのPin指定モードをBCMへ設定
                GPIO.setmode(GPIO.BCM)
                #------  使用するピンの入出力宣言
                #出力ピン
                GPIO.setup(TempGui._CNT0, GPIO.OUT) #GPIO22 出力 CNT0
                GPIO.setup(TempGui._CNT1, GPIO.OUT) #GPIO23 出力 CNT1
                GPIO.setup(TempGui._CNT2, GPIO.OUT) #GPIO24 出力 CNT2
                #入力ピン
                GPIO.setup(TempGui._SW_FN, GPIO.IN, pull_up_down = GPIO.PUD_UP) #GPIO25 入力　SW Pullup
                GPIO.setup(TempGui._EMO_SW, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) #GPIO26 入力　EMO Pulldown
                #出力ピンの初期値設定
                GPIO.output(TempGui._CNT0, 0)      #Lo出力
                GPIO.output(TempGui._CNT1, 0)      #Lo出力
                GPIO.output(TempGui._CNT2, 0)      #Lo出力0

            #----------------------------------------------
            def set_led_mode(self, cnt2 ,cnt1 ,cnt0):
                """000:スタンバイ ,001青, 010緑, 011加熱中表示, 100加熱保温中, 101加熱完了呼び出し"""

                #出力ピンの初期値設定
                GPIO.output(TempGui._CNT0, cnt0)      #Lo出力
                GPIO.output(TempGui._CNT1, cnt1)      #Lo出力
                GPIO.output(TempGui._CNT2, cnt2)      #Lo出力

            #----------------------------------------------
            def emo_check(self):
                if ((GPIO.input(TempGui._EMO_SW) == 0)):
                    #EMOスイッチを検出するとプログラムループがここで止まる→Arduinoはタイムアウトで加熱停止
                    messagebox.showwarning("EMO", "EMO Switch Detected! System is LOCKED!")

            #----------------------------------------------
            def start_sw_check(self):
                """Function スイッチの入力検出(一致検出の結果を１回だけ返してデフォルトを保持する)"""
                self.sw_state = 1                             #呼び出し元に値を渡す変数初期化
                if ( (GPIO.input(TempGui._SW_FN)) == 0 ):     #スイッチの状態を取得
                    time.sleep(0.1)                           #100ms待つ
                    self.naga_oshi_kenshutu += 1              #長押し検出カウンターインクリメント
                    if ( (GPIO.input(TempGui._SW_FN)) == 0 ): #もう一度スイッチを見る
                        if (self.sw_previous_state == 1 ):    #前回のスイッチ状態がOFFのとき
                            self.sw_previous_state = 0        #前回のスイッチがONになったよフラグ
                            self.sw_state = 0                 #呼び出し元に値を渡す変数にONフラグ格納
                            print("Function SW Detect ")      #スイッチ・オン表示
                else:
                    self.sw_previous_state = 1               #ツイッチがOFFだったら前回の状態をOFFに設定
                    self.naga_oshi_kenshutu = 0              #長押し検出カウンターリセット

                return(self.sw_state)                        #スイッチの状態を返す

            #-----------------------------------------------
            def get_nagaoshi_state(self):
                """長押し検出カウンターの値を返す関数"""
                return(self.naga_oshi_kenshutu)










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
            def set_state(self,state):
                #外部スイッチのＵＩ「ＯＮ」表示
                if (state == 1):
                    self.label_on_off["text"] = "ON"
                    self.label_on_off["bg"] = "red"
                    self.label_on_off.relief=tkinter.RAISED
                if (state == 0):
                    #外部スイッチのＵＩ「ＯＦＦ」表示
                    self.label_on_off["text"] = "OFF"
                    self.label_on_off["bg"] = "green"
                    self.label_on_off.relief=tkinter.SUNKEN

        #-----------------------------------------------------------------------------
        class ArduinoDataFrame(object):
            """全ArduinoのUIを定義するClass"""
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
                self.heater_workdet0 = HeaterIndicatorFrame(arduino0_fraeme, "ワーク検出")
                self.heater_enable0 = HeaterIndicatorFrame(arduino0_fraeme, "加熱許可")
                self.heater_state0 = HeaterIndicatorFrame(arduino0_fraeme, "ヒーターON/OFF")
                self.heater_reach0 = HeaterIndicatorFrame(arduino0_fraeme, "温度到達")

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
                self.heater_workdet1 = HeaterIndicatorFrame(arduino1_fraeme, "ワーク検出")
                self.heater_enable1 = HeaterIndicatorFrame(arduino1_fraeme, "加熱許可")
                self.heater_state1 = HeaterIndicatorFrame(arduino1_fraeme, "ヒーターON/OFF")
                self.heater_reach1 = HeaterIndicatorFrame(arduino1_fraeme, "温度到達")

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
                self.heater_workdet2 = HeaterIndicatorFrame(arduino2_fraeme, "ワーク検出")
                self.heater_enable2 = HeaterIndicatorFrame(arduino2_fraeme, "加熱許可")
                self.heater_state2 = HeaterIndicatorFrame(arduino2_fraeme, "ヒーターON/OFF")
                self.heater_reach2 = HeaterIndicatorFrame(arduino2_fraeme, "温度到達")
#-------
            def main_ui_update(self):
                #Arduino 0
                self.ir_temp0.change_value(TempGui.arduino_param_0['ir_temp'])
                self.amb_temp0.change_value(TempGui.arduino_param_0['ambient_temp'])
                self.distance0.change_distance(TempGui.arduino_param_0['distance'])
                self.cnt_target0.set_target_value(TempGui.arduino_param_0['target_temp'])
                self.heater_workdet0.set_state(TempGui.arduino_param_0['work_det'])
                self.heater_enable0.set_state(TempGui.arduino_param_0['heater_enable'])
                self.heater_state0.set_state(TempGui.arduino_param_0['heater_condition'])
                self.heater_reach0.set_state(TempGui.arduino_param_0['temp_reach'])
                #Arduino 1
                self.ir_temp1.change_value(TempGui.arduino_param_1['ir_temp'])
                self.amb_temp1.change_value(TempGui.arduino_param_1['ambient_temp'])
                self.distance1.change_distance(TempGui.arduino_param_1['distance'])
                self.cnt_target1.set_target_value(TempGui.arduino_param_1['target_temp'])
                self.heater_workdet1.set_state(TempGui.arduino_param_1['work_det'])
                self.heater_enable1.set_state(TempGui.arduino_param_1['heater_enable'])
                self.heater_state1.set_state(TempGui.arduino_param_1['heater_condition'])
                self.heater_reach1.set_state(TempGui.arduino_param_1['temp_reach'])
                #Arduino 0
                self.ir_temp2.change_value(TempGui.arduino_param_2['ir_temp'])
                self.amb_temp2.change_value(TempGui.arduino_param_2['ambient_temp'])
                self.distance2.change_distance(TempGui.arduino_param_2['distance'])
                self.cnt_target2.set_target_value(TempGui.arduino_param_2['target_temp'])
                self.heater_workdet2.set_state(TempGui.arduino_param_2['work_det'])
                self.heater_enable2.set_state(TempGui.arduino_param_2['heater_enable'])
                self.heater_state2.set_state(TempGui.arduino_param_2['heater_condition'])
                self.heater_reach2.set_state(TempGui.arduino_param_2['temp_reach'])

#----------------------------------------------------
#-------まだTopLevelClassの__init__は続くよ
        self.num = 0
        self.naga_oshi_kenshutu = 0

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
        self.s_machine = StateMachine("yani")    #ステートマシンオブジェクト生成
        self.main_ui.main_ui_update()            #UIの値を親グラス変数の値にアップデート（初期化）

        self.update()

    #---温度の更新

    def update(self):
        """100ms/１回の更新頻度"""
        #Arduino0,1,2のデータ取得（SPI Read）
        self.arduino0_data = self.ardu0.GetDataArd()
        self.arduino1_data = self.ardu1.GetDataArd()
        self.arduino2_data = self.ardu2.GetDataArd()

        #Arduinoから取得した値をClass変数に格納する
        self.arduino_param_0['ir_temp'] = (self.arduino0_data)[0]   #放射温度計
        self.arduino_param_1['ir_temp'] = (self.arduino1_data)[0]
        self.arduino_param_2['ir_temp'] = (self.arduino2_data)[0]
        self.arduino_param_0['ambient_temp'] = (self.arduino0_data)[1]   #周辺温度
        self.arduino_param_1['ambient_temp'] = (self.arduino1_data)[1]
        self.arduino_param_2['ambient_temp'] = (self.arduino2_data)[1]
        self.arduino_param_0['distance'] = (self.arduino0_data)[2]   #距離計データ
        self.arduino_param_1['distance'] = (self.arduino1_data)[2]
        self.arduino_param_2['distance'] = (self.arduino2_data)[2]
        #UIから設定されたターゲット温度を取得
        self.arduino_param_0['target_temp'] = self.main_ui.cnt_target0.get_target_value()
        self.arduino_param_1['target_temp'] = self.main_ui.cnt_target1.get_target_value()
        self.arduino_param_2['target_temp'] = self.main_ui.cnt_target2.get_target_value()
        #UIから取得したターゲット温度をArduinoに転送
        self.ardu0.SetTempTarget(self.arduino_param_0['target_temp'])
        self.ardu1.SetTempTarget(self.arduino_param_1['target_temp'])
        self.ardu2.SetTempTarget(self.arduino_param_2['target_temp'])
        #-----------------------------
        self.main_ui.main_ui_update()            #UIの値を親グラス変数の値にアップデート

        #---------------------------------
        #--- コントロールBOXのスイッチ類の値取得
        #---------------------------------
        self.usr_cnt.emo_check()
        self.fn_sw_state = self.usr_cnt.start_sw_check()

        #--------------------------------
        #---   ステートマシンの状態遷移（未整理べた書き、なんとかしましょう）
        #-------------------------------
        #Func_SWの値取得
        #------------------
        #ワークの有無検出
        if ((self.arduino_param_0['distance']) <= 100): #ヒーター1が50mm以内
            self.arduino_param_0['work_det'] = True
        else:
            self.arduino_param_0['work_det'] = False

        if ((self.arduino_param_1['distance']) <= 150):#ヒーター2が100mm以内
            self.arduino_param_1['work_det'] = True
        else:
            self.arduino_param_1['work_det'] = False

        if ((self.arduino_param_2['distance']) <= 150):#ヒーター3が150mm以内
            self.arduino_param_2['work_det'] = True
        else:
            self.arduino_param_2['work_det'] = False

        #もし距離センサーで近接状態を検出したら(測距中以外の動作をここに記述)
        if (((self.s_machine.state)== 'idle') or ((self.s_machine.state)== 'heat') or ((self.s_machine.state)== 'keep') or ((self.s_machine.state)== 'finish')):
            if (((self.arduino_param_0['distance']) <= self.PROXIMILITTY_LIMIT) or ((self.arduino_param_1['distance']) <= self.PROXIMILITTY_LIMIT) or ((self.arduino_param_2['distance']) <= self.PROXIMILITTY_LIMIT) ):
                self.s_machine.too_close()
                self.usr_cnt.set_led_mode(0,1,1)
                print(self.s_machine.state)
        #近接エラーフラグが立っていたら復帰フラグ監視モードへ
        if ((self.s_machine.state) == 'proximity_error'):
            if (((self.arduino_param_0['distance']) > self.PROXIMILITTY_LIMIT) and ((self.arduino_param_1['distance']) > self.PROXIMILITTY_LIMIT) and ((self.arduino_param_2['distance']) > self.PROXIMILITTY_LIMIT) ):
                self.s_machine.close_releace()
                self.usr_cnt.set_led_mode(0,0,0)

        #-------------------------------
        #    Idle ステート時の処理
        if ((self.s_machine.state)== 'idle'):
            """State = 'idleのときの処理"""
            # UIのBOOLスイッチの値を初期化
            self.arduino_param_0['heater_condition'] = bool(self.ardu0.GetHeaterCondition()[0])
            self.arduino_param_1['heater_condition'] = bool(self.ardu1.GetHeaterCondition()[0])
            self.arduino_param_2['heater_condition'] = bool(self.ardu2.GetHeaterCondition()[0])

            self.arduino_param_0['heater_enable'] = False
            self.arduino_param_1['heater_enable'] = False
            self.arduino_param_2['heater_enable'] = False

            self.arduino_param_0['temp_reach'] = False
            self.arduino_param_1['temp_reach'] = False
            self.arduino_param_2['temp_reach'] = False
            #タイマー用変数の初期化
            self.time = 0
            self.past_time = 0
            self.cycle_time = 0
            #スイッチが押されたらの処理
            if (not(self.fn_sw_state)):
                self.fn_sw_state = 1
                # スイッチON時の処理をここに記述
                print ("SW ON")
                self.s_machine.func_sw() #次のステートへ
                self.usr_cnt.set_led_mode(0,0,1)
                print(self.s_machine.state)

        #------------------
        if((self.s_machine.state)== 'meas_dist'):
            """state = meas_distのときの処理"""
            if(self.arduino_param_0['distance'] <= 100):
                self.s_machine.in_range()
                self.usr_cnt.set_led_mode(0,1,0)
                print(self.s_machine.state)

        #------------------
        if((self.s_machine.state)== 'ready'):
            """state = readyのときの処理"""
            if(self.arduino_param_0['distance'] > 100 ):
                self.s_machine.out_range()
                self.usr_cnt.set_led_mode(0,0,1)
                print(self.s_machine.state)
            if((self.arduino_param_0['distance'] <= self.PROXIMILITTY_LIMIT)):
                self.s_machine.too_short()
                self.usr_cnt.set_led_mode(0,1,1)
                print(self.s_machine.state)
            if (not(self.fn_sw_state)):
                self.fn_sw_state = 1
                print ("SW ON")
                self.s_machine.func_sw()
                self.usr_cnt.set_led_mode(1,0,0)
                #加熱ステート移動の前にヒーター何本加熱するか検出
                if ((self.arduino_param_0['distance']) <= 100): #ヒーター1が50mm以内
                    self.arduino_param_0['heater_enable'] = True
                    if ((self.arduino_param_1['distance']) <= 150):#ヒーター2が100mm以内
                        self.arduino_param_1['heater_enable'] = True
                        if ((self.arduino_param_2['distance']) <= 150):#ヒーター3が150mm以内
                            self.arduino_param_2['heater_enable'] = True
                print(self.s_machine.state)

        #------------------
        #近接警告
        if((self.s_machine.state)== 'proximity'):
            """state = proximityのときの処理"""
            if((self.arduino_param_0['distance'] > 50)):
                self.s_machine.in_range()
                self.usr_cnt.set_led_mode(0,1,0)
                print(self.s_machine.state)

        #------------------
        #heat の処理
        if((self.s_machine.state)== 'heat'):
            #
            #タイムアウト処理を追加する必要がある
            #
            #
            #EnableフラグのあるヒーターのみONする
            if (self.arduino_param_0['heater_enable']): #ヒーター1が50mm以内
                self.ardu0.SetHeatEnableFlag()     #ヒーター1の加熱許可フラグ
                #温度判定
                self.arduino_param_0['temp_reach'] = bool(self.ardu0.GetTempReach()[0])
                print(self.ardu0.GetTempReach())
            else:
                #温度到達フラグTrue
                self.arduino_param_0['temp_reach'] = True
            #------------
            if (self.arduino_param_1['heater_enable']):#ヒーター2が100mm以内
                self.ardu1.SetHeatEnableFlag()     #ヒーター2の加熱許可フラグ
                #温度判定
                self.arduino_param_1['temp_reach'] = bool(self.ardu1.GetTempReach()[0])
            else:
                #温度到達フラグTrue
                self.arduino_param_1['temp_reach'] = True
                #------------
            if (self.arduino_param_2['heater_enable']):#ヒーター3が150mm以内
                self.ardu2.SetHeatEnableFlag()     #ヒーター3の加熱許可フラグ
                #温度判定
                self.arduino_param_2['temp_reach'] = bool(self.ardu2.GetTempReach()[0])
            else:
                #温度到達フラグTrue
                self.arduino_param_2['temp_reach'] = True
            #------------
            #HeaterのUI用の変数を更新
            self.arduino_param_0['heater_condition'] = bool(self.ardu0.GetHeaterCondition()[0])
            self.arduino_param_1['heater_condition'] = bool(self.ardu1.GetHeaterCondition()[0])
            self.arduino_param_2['heater_condition'] = bool(self.ardu2.GetHeaterCondition()[0])
            #加熱完了フラグ読み取り（すべての稼働中ヒーターが温度到達したら次）
            if (self.arduino_param_0['temp_reach'] and self.arduino_param_1['temp_reach'] and self.arduino_param_2['temp_reach']):
                self.s_machine.temp_reach()
                self.usr_cnt.set_led_mode(1,0,1)
                print(self.s_machine.state)


            pass
        #------------------
        #keep の処理
        if((self.s_machine.state)== 'keep'):
            #HeaterのUI用の変数を更新
            #EnableフラグのあるヒーターのみONする
            if (self.arduino_param_0['heater_enable']): #ヒーター1が50mm以内
                self.ardu0.SetHeatEnableFlag()     #ヒーター1の加熱許可フラグ
                #温度判定
                self.arduino_param_0['temp_reach'] = bool(self.ardu0.GetTempReach()[0])
            else:
                #温度到達フラグTrue
                self.arduino_param_0['temp_reach'] = True
            #------------
            if (self.arduino_param_1['heater_enable']):#ヒーター2が100mm以内
                self.ardu1.SetHeatEnableFlag()     #ヒーター2の加熱許可フラグ
                #温度判定
                self.arduino_param_1['temp_reach'] = bool(self.ardu1.GetTempReach()[0])
            else:
                #温度到達フラグTrue
                self.arduino_param_1['temp_reach'] = True
                #------------
            if (self.arduino_param_2['heater_enable']):#ヒーター3が150mm以内
                self.ardu2.SetHeatEnableFlag()     #ヒーター3の加熱許可フラグ
                #温度判定
                self.arduino_param_2['temp_reach'] = bool(self.ardu2.GetTempReach()[0])
            else:
                #温度到達フラグTrue
                self.arduino_param_2['temp_reach'] = True
            #------------
            #HeaterのUI用の変数を更新
            self.arduino_param_0['heater_condition'] = bool(self.ardu0.GetHeaterCondition()[0])
            self.arduino_param_1['heater_condition'] = bool(self.ardu1.GetHeaterCondition()[0])
            self.arduino_param_2['heater_condition'] = bool(self.ardu2.GetHeaterCondition()[0])
            #加熱完了フラグ読み取り（すべての稼働中ヒーターが温度到達したら次）
            if (self.arduino_param_0['temp_reach'] and self.arduino_param_1['temp_reach'] and self.arduino_param_2['temp_reach']):
                #温度維持時間をカウントする
                if (self.time == 0):
                    self.time = time.time()
                else:
                    pass

                self.cycle_time = time.time() - self.time
                self.past_time = self.past_time + self.cycle_time
                self.time = time.time()
                print(self.past_time)
            pass

            if (self.past_time >= 30 ) :
                self.s_machine.timer()
                self.usr_cnt.set_led_mode(1,1,0)
                print(self.s_machine.state)
            pass

        #------------------
        #finish の処理
        if((self.s_machine.state)== 'finish'):
            #アラーム呼び出し、FnSW待ち
            #EnableフラグのあるヒーターのみONする
            if (self.arduino_param_0['heater_enable']): #ヒーター1が50mm以内
                self.ardu0.SetHeatEnableFlag()     #ヒーター1の加熱許可フラグ
                #温度判定
                self.arduino_param_0['temp_reach'] = bool(self.ardu0.GetTempReach()[0])
            else:
                #温度到達フラグTrue
                self.arduino_param_0['temp_reach'] = True
            #------------
            if (self.arduino_param_1['heater_enable']):#ヒーター2が100mm以内
                self.ardu1.SetHeatEnableFlag()     #ヒーター2の加熱許可フラグ
                #温度判定
                self.arduino_param_1['temp_reach'] = bool(self.ardu1.GetTempReach()[0])
            else:
                #温度到達フラグTrue
                self.arduino_param_1['temp_reach'] = True
                #------------
            if (self.arduino_param_2['heater_enable']):#ヒーター3が150mm以内
                self.ardu2.SetHeatEnableFlag()     #ヒーター3の加熱許可フラグ
                #温度判定
                self.arduino_param_2['temp_reach'] = bool(self.ardu2.GetTempReach()[0])
            else:
                #温度到達フラグTrue
                self.arduino_param_2['temp_reach'] = True
            #------------
            #HeaterのUI用の変数を更新
            self.arduino_param_0['heater_condition'] = bool(self.ardu0.GetHeaterCondition()[0])
            self.arduino_param_1['heater_condition'] = bool(self.ardu1.GetHeaterCondition()[0])
            self.arduino_param_2['heater_condition'] = bool(self.ardu2.GetHeaterCondition()[0])
            #------------
            if (not(self.fn_sw_state)):
                self.s_machine.func_sw()
                self.usr_cnt.set_led_mode(0,0,0)
            pass

        #------------------
        if (self.usr_cnt.get_nagaoshi_state() == 10 ) :
            #スイッチ長押し時の処理をここに記述
            print("長押し検出")
            self.s_machine.long_press()
            self.usr_cnt.set_led_mode(0,0,0)
            print(self.s_machine.state)



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
            #- プログラム停止後の初期化処理
            #GPIOの初期化
            GPIO.cleanup()

    root.protocol("WM_DELETE_WINDOW", on_closing)
#------------------------------------------
#----------------------------------

    root.mainloop()
