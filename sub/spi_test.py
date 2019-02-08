#! /usr/bin/env python3
# coding: UTF-8
#ラベルの表示確認
#2019.01.16 by SGR

from datetime import datetime
import spidev
from time import sleep

def printbits(data, padding=8):
    template = '{{:0{}b}}'.format(padding)
    for d in data:
        print(template.format(d))

def spisetup():
    spi = spidev.SpiDev()
    spi.open(0, 0)        #SPI0 : SPIのチャネル設定
#    spi.open(0, 1)        #SPI1 : SPIのチャネル設定
    spi.max_speed_hz = 1000000
    spi.bits_per_word = 8
    spi.mode = 0
#   spi.xfer([0x80, 0b00010010])             # write configuration
    #printbits(spi.xfer([0x00, 0x00])[1:])   # read configuration
    return spi
def spiread(spi, r_ref=430):
#------ Write test  アドレス0x81にデータ0x51を書き込み,ラーゲット温度129℃設定
    spi.xfer([0x81])             # v-bias on
    sleep(0.1)                               # wait for saving to register
    bits = spi.xfer([0x81]) # read bits
    print("ReadResult=",int(bits[0]))

    spi.xfer([0x01])             # v-bias on
    sleep(0.1)                               # wait for saving to register
    bits = spi.xfer([0x00]) # read bits
    print(int(bits[0]))

    spi.xfer([0x02])             # v-bias on
    sleep(0.1)                               # wait for saving to register
    bits = spi.xfer([0x00]) # read bits
    print(int(bits[0]))

    spi.xfer([0x03])             # v-bias on
    sleep(0.1)                               # wait for saving to register
    bits = spi.xfer([0x00]) # read bits
    print(int(bits[0]))

    spi.xfer([0x04])             # v-bias on
    sleep(0.1)                               # wait for saving to register
    bits = spi.xfer([0x00]) # read bits
    print(int(bits[0]))

#------ Write test  アドレス0x81にデータ0x32を書き込み,ターゲット温度50℃設定
    spi.xfer([0x81])             # v-bias on
    sleep(0.1)                               # wait for saving to register
    bits = spi.xfer([0x32]) # read bits
    print("ReadResult=",int(bits[0]))


#    spi.xfer([0x80, 0b00010010])             # v-bias off
#    adc = bits[0] << 7 | bits[1] >> 1        # make 15 bits
    #printbits(bits)
    #printbits([adc], padding=15)
    #r_rtd = (adc * r_ref) / 2 ** 15
    #print('r_rtd:{}ohm'.format(r_rtd))
#    adc = adc * r_ref / 400                  # convert adc on r_ref == 400
#    temperature = adc / 32 - 256             # convert adc to temperature

    return 123

def spiquit(spi):
    spi.close()

#------------------------------------------------------------------------
if __name__ == '__main__':
    try:
        spi = spisetup()
        while True:
            tempareture = spiread(spi)
            print('{:%Y-%m-%d %H:%M:%S} temp {:5.2f}'.format(
                datetime.now(), tempareture))
            sleep(5)
    except KeyboardInterrupt:
        spiquit(spi)
        exit(0)
