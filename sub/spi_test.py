#! /usr/bin/env python3
# coding: UTF-8
#ラベルの表示確認
#2019.01.16 by SGR

from datetime import datetime
import spidev
from time import sleep

#----------
class SpiDev(object):
    """SPI通信を行うオブジェクトを生成する"""
    def __init__(self, devide_number):
        """SPIデバイスの生成。devide_numberでSPIの0 or 1を選択する"""
        self.spi = spidev.SpiDev()           #オブジェクト生成
        self.dev_num = devide_number         #引数から内部変数に引き渡し
        self.spi.open(0, self.dev_num)       #dev_num : SPIのチャネル設定
        self.spi.max_speed_hz = 1000000      #SPIの最大レート
        self.spi.bits_per_word = 8           #送受信単位Bit（１Byte)
        self.spi.mode = 0                    #0:立ち上がりエッジ、1:立ち下がりエッジ

#----------
    def spi_read(self, read_addres):
        """IPS DATAの書き込み,読み取りアドレス送信後、0x00(ダミーデータ)を送信しながら読み取り"""
        self.spi.xfer([read_addres])             # 読み取るアドレスの指定
        sleep(0.1)                               # wait for saving to register
        bits = self.spi.xfer([0x00]) # read bitsダミーデータ0x00を書きながら読む
        return bits

#----------
    def spi_write(self, w_address, w_data):
        """w_address=書き込みアドレス, w_data＝書き込みデータ"""
        spi.xfer([w_address])             # v-bias on
        sleep(0.1)                        # wait for saving to register
        bits = spi.xfer([w_data]) # read bits
#        print("ReadResult=",int(bits[0]))
        return bits
#-----------
    def spiquit(self):
        """SPIのクローズ"""
        self.spi.close()

#------------------------------------------------------------------------
if __name__ == '__main__':
#    try:
        spi0 = SpiDev(0)
        spi1 = SpiDev(1)
        while True:
            #-----温度取得 SPIデバイス 0-----
            temp0_lsb = spi0.spi_read(0x01)    # 温度の下位８Bit
            temp0_msb = (spi0.spi_read(0x02) ) # 温度の上位８Bit
            temp0 =(((temp0_msb[0] << 8)  + temp0_lsb[0] ) / 100 )
            print("TEMP0 = ", temp0)
            #
            amb_temp0_lsb = spi0.spi_read(0x03)    # 温度の下位８Bit
            amb_temp0_msb = (spi0.spi_read(0x04) ) # 温度の上位８Bit
            amb_temp0 =(((amb_temp0_msb[0] << 8)  + amb_temp0_lsb[0] ) / 100 )
            print("Amb_TEMP0 = ", amb_temp0)
            #
            dist0_lsb = spi0.spi_read(0x05)    # 温度の下位８Bit
            dist0_msb = (spi0.spi_read(0x06) ) # 温度の上位８Bit
            dist0 =((dist0_msb[0] << 8)  + dist0_lsb[0] )
            print("Dintance0 = ", dist0)
            #
            #-----温度取得 SPI デバイス 1-----
            temp1_lsb = spi1.spi_read(0x01)    # 温度の下位８Bit
            temp1_msb = (spi1.spi_read(0x02) ) # 温度の上位８Bit
            temp1 =(((temp1_msb[0] << 8)  + temp1_lsb[0] ) / 100 )
            print("TEMP1 = ", temp1)
            #
            amb_temp1_lsb = spi1.spi_read(0x03)    # 温度の下位８Bit
            amb_temp1_msb = (spi1.spi_read(0x04) ) # 温度の上位８Bit
            amb_temp1 =(((amb_temp1_msb[0] << 8)  + amb_temp1_lsb[0] ) / 100 )
            print("Amb_TEMP1 = ", amb_temp1)
            #
            dist1_lsb = spi1.spi_read(0x05)    # 温度の下位８Bit
            dist1_msb = (spi1.spi_read(0x06) ) # 温度の上位８Bit
            dist1 =((dist1_msb[0] << 8)  + dist1_lsb[0] )
            print("Dintance1 = ", dist1)
            #
            sleep(1)
#    except KeyboardInterrupt:
        spi.spiquit()
        exit(0)
