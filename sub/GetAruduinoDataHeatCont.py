#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 脂盛ヒータコントローラー専用クラス
# 転用禁止

from sub.SpiRW import SpiRW
from time import sleep

class GetAruduinoDataHeatCnt(SpiRW):
    """親クラス SpiDev、デバイス生成とデータの処理を追記"""
    def GetDataArd(self):
            #-----温度取得 SPIデバイス 0-----
        self.temp_lsb = self.spi_read(0x01)    # 温度の下位８Bit
        self.temp_msb = self.spi_read(0x02)    # 温度の上位８Bit
        self.temp =(((self.temp_msb[0] << 8)  + self.temp_lsb[0] ) / 100 )
#           print("TEMP0 = ", temp0)
            #
        self.amb_temp_lsb = self.spi_read(0x03)    # 温度の下位８Bit
        self.amb_temp_msb = self.spi_read(0x04)  # 温度の上位８Bit
        self.amb_temp =(((self.amb_temp_msb[0] << 8)  + self.amb_temp_lsb[0] ) / 100 )
#            print("Amb_TEMP0 = ", self.amb_temp0)
            #
        self.dist_lsb = self.spi_read(0x05)    # 温度の下位８Bit
        self.dist_msb = self.spi_read(0x06)  # 温度の上位８Bit
        self.dist =((self.dist_msb[0] << 8)  + self.dist_lsb[0] )
#            print("Dintance0 = ", self.dist0)
            #
        return (self.temp, self.amb_temp, self.dist)

    def SetTempTarget(self, temp):
        """温度は℃で転送する"""
        self.spi_write(0x81, temp)
    def SetTempHis(self, temp):
        """ヒステリシス温度は℃で転送する"""
        self.spi_write(0x82, temp)
    def SetDistanceLimit(self, distance):
        """距離はcm単位で転送する"""
        self.spi_write(0x83, distance)

#------------------------------------------------
if __name__ == '__main__':
    ard0 = GetAruduinoDataHeatCnt(8,0) # 8Byte単位でデバイス0番
    ard1 = GetAruduinoDataHeatCnt(8,1) # 8Byte単位でデバイス0番
    i = 0

    while 1:
        i+=1
        print("Arduino0", ard0.GetDataArd())
        print("Arduino1", ard1.GetDataArd())
        print(i)
        ard0.SetTempTarget(i)
        sleep(1)
