#!/usr/bin/env python
# -*- coding: utf-8 -*-
#HAMAMATSU Photon S11059 ColorSenser

import smbus
import time
import RPi.GPIO as GPIO
import gc

i2c = smbus.SMBus(1) #コネクションオブジェクト生成　

#デバイスのスレイブアドレス
address_S11059 = 0x2a #浜フォトカラーセンサー
address_AM2320 = 0x5c #温度湿度センサー

#GPIOのセッティング
GPIO.setmode(GPIO.BCM)  #GPIO BMC定義
GPIO.setup(17,GPIO.OUT) #GPIO17 出力モード


# 以下　センサー読み出し・ループ
while True:

    GPIO.output(17,GPIO.HIGH) #GPIO17Hi出力

# センサsleep解除
    try:
        i2c.write_i2c_block_data(address_AM2320,0x00,[])
    except:
        pass
# 読み取り命令
    time.sleep(0.003)
    i2c.write_i2c_block_data(address,0x03,[0x00,0x04])

# データ受取
    time.sleep(0.015)
    block = i2c.read_i2c_block_data(address,0,6)
    hum = float(block[2] << 8 | block[3])/10
    tmp = float(block[4] << 8 | block[5])/10

    print('hum=%.2f'  %hum) # 湿度表示
    print('Temp=%.2f' %tmp) # 温度表示

    time.sleep(0.1)
    GPIO.output(17,GPIO.LOW) #GPIO17Lo出力

#　取得後の待機時間
    time.sleep(1)

    del hum,tmp
    gc.collect()

GPIO.cleanup() #GPIO　初期化