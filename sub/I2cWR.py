#! /usr/bin/env python
# coding: UTF-8
#ラベルの表示確認
#2019.01.16 by SGR
#---- import ------
import smbus
import time

#------- class
class I2cWR(object):
    def __init__(self, dvice_adress):
        self._dvice_adress = dvice_adress
        self.i2c = smbus.SMBus(1)
        self._r_data = 0x00
    #------  Data Write
    def i2c_data_w(self, write_adress,w_data):
#        self._adress = writeAdress
        self.i2c.write_i2c_block_data(self._dvice_adress, write_adress, w_data)
    #------ I2c Data Read
    def i2c_data_r(self, read_start, read_end):
        self._r_data = self.i2c.read_i2c_block_data(self._dviceAdress, read_start, read_end)
        return self._rData

###############################
if __name__ == '__main__':
    #am2320オブジェクト生成
    am2320_tmp = I2cWR(0x5c)

    # センサsleep解除
    try:
        am2320_tmp.i2c_data_w(0x00,[])
        #i2cAm2320.write_i2c_block_data(address,0x00,[])
    except:
        pass

    # 読み取り命令
    time.sleep(0.003)
    am2320_tmp.i2c_data_w(0x03,[0x00,0x04])
    # データ受取
    time.sleep(0.015)
    block = am2320_tmp.i2c_data_r(0,6)
    hum = float(block[2] << 8 | block[3])/10
    tmp = float(block[4] << 8 | block[5])/10

    print('hum=%.2f'  %hum) # 湿度表示
    print('Temp=%.2f' %tmp) # 温度表示
