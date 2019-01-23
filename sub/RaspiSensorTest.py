#!/usr/bin/env python
# -*- coding: utf-8 -*-
#HAMAMATSU Photon S11059 ColorSenser

#import RPi.GPIO as GPIO
import time
from sub.I2cWR import I2cWR #\I2cWR.py

class RaspiSensorTest(object):
    #デバイスのスレイブアドレス
#    _address_s11059 = 0x2a #浜フォトカラーセンサー
    _address_am2320 = 0x5c #温度湿度センサー

    def __init__(self):
        #--initial settimg---

        #各センサーオブジェクトを生成
#       self.s11059 = I2cWR(self._address_s11059)
        self.am2320 = I2cWR(self._address_am2320)

        #s11059センサー初期設定-----
        time.sleep(0.003)
        #初期設定
#        self.s11059.i2c_data_w(0x00,[0xe4,0x06,0x04])
#        time.sleep(0.003)
#-----------------------------------------------------
    def get_data(self):

        # 以下　センサー読み出し・ループ
#        GPIO.output(17,GPIO.HIGH) #GPIO17Hi出力
        #---センサー読みだし-------
        try:
            self.am2320.i2c_data_w(0x00,[])
        except:
            pass

        # 読み取り命令
        time.sleep(0.003)
        self.am2320.i2c_data_w(0x03,[0x00,0x04])
        # データ受取
        time.sleep(0.015)
        block = self.am2320.i2c_data_r(0,6)
        i=[7,8,9]
        self._hum = float(block[2] << 8 | block[3])/10
        self._tmp = float(block[4] << 8 | block[5])/10
#
#------ s11059読み出し------
#
        """ #光センサーは使っていないのでマスク
        try:
            self.s11059.i2c_data_w(0x00,[])
            #i2cAm2320.write_i2c_block_data(address,0x00,[])
        except:
            pass

        # 読み取り命令

        #レジスタリセット
        self.s11059.i2c_data_w(0x00,[0x84])
        #リセット解除
        time.sleep(0.015)
        self.s11059.i2c_data_w(0x00,[0x04])
        time.sleep(1)
        block = self.s11059.i2c_data_r(3,8)

        r = block[0] << 8 | block[1]
        g = block[2] << 8 | block[3]
        b = block[4] << 8 | block[5]
        ir = block[6] << 8 | block[7]
#        print(' R : {:d}'.format(r)  )
#        print(' G : {:d}'.format(g)  )
#        print(' B : {:d}'.format(b)  )
#        print('IR : {:d}'.format(ir) )

#
#-------------------------------------
#
        time.sleep(0.1)
#        GPIO.output(17,GPIO.LOW) #GPIO17Lo出力
#取得後の待機時間
        time.sleep(0.01)
        """
        return [self._tmp, self._hum]
#        return 1, 2
#------------------------------------------------
if __name__ == '__main__':
    root=tkinter.Tk()
    app=RaspiSensorTest()
    main()
    root.mainloop()
