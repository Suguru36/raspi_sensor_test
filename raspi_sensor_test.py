#!/usr/bin/env python
# -*- coding: utf-8 -*-
#HAMAMATSU Photon S11059 ColorSenser

import RPi.GPIO as GPIO
import time

from sub.I2cWR import I2cWR #sub\i2cWR.py
from sub.TempGui import TempGui #sub/temp

#--initial settimg---
#
#デバイスのスレイブアドレス
address_S11059 = 0x2a #浜フォトカラーセンサー
address_AM2320 = 0x5c #温度湿度センサー

#GPIOのセッティング
GPIO.setmode(GPIO.BCM)  #GPIO BMC定義
GPIO.setup(17,GPIO.OUT) #GPIO17 出力モード

#UIを生成
mainUi = TempGui()

#各センサーオブジェクトを生成
s11059 = I2cWR(address_S11059)
am2320 = I2cWR(address_AM2320)

#s11059センサー初期設定-----
time.sleep(0.003)
#初期設定
s11059.i2cDataW(0x00,[0xe4,0x06,0x04])
time.sleep(0.003)

# 以下　センサー読み出し・ループ
while True:
    GPIO.output(17,GPIO.HIGH) #GPIO17Hi出力
#---センサー読みだし-------
    try:
        am2320.i2cDataW(0x00,[])
        #i2cAm2320.write_i2c_block_data(address,0x00,[])
    except:
        pass

    # 読み取り命令
    time.sleep(0.003)
    am2320.i2cDataW(0x03,[0x00,0x04])
    # データ受取
    time.sleep(0.015)
    block=am2320.i2cDataR(0,6)
    i=[7,8,9]
    hum = float(block[2] << 8 | block[3])/10
    tmp = float(block[4] << 8 | block[5])/10
    print('hum=%.2f'  %hum) # 湿度表示
    print('Temp=%.2f' %tmp) # 温度表示

#
#------ s11059読み出し------
#
    try:
        s11059.i2cDataW(0x00,[])
        #i2cAm2320.write_i2c_block_data(address,0x00,[])
    except:
        pass

    # 読み取り命令

    #レジスタリセット
    s11059.i2cDataW(0x00,[0x84])
    #リセット解除
    time.sleep(0.015)
    s11059.i2cDataW(0x00,[0x04])
    time.sleep(1)
    block=s11059.i2cDataR(3,8)

    r = block[0] << 8 | block[1]
    g = block[2] << 8 | block[3]
    b = block[4] << 8 | block[5]
    ir = block[6] << 8 | block[7]
    print(' R : {:d}'.format(r)  )
    print(' G : {:d}'.format(g)  )
    print(' B : {:d}'.format(b)  )
    print('IR : {:d}'.format(ir) )

#
#-------------------------------------
#
    time.sleep(0.1)
    GPIO.output(17,GPIO.LOW) #GPIO17Lo出力
#取得後の待機時間
    time.sleep(0.01)

GPIO.cleanup() #GPIO　初期化
