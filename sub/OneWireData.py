#~/python_apps/w1-test.py
# -*- coding: utf-8 -*-
import os
import glob
import time
import subprocess

class OneWireDataRead(object):
    """1-Wireインターフェイスの28********のデータファイルを読んで返す"""
    def __init__(self):
        os.system('modprobe w1-gpio')
        os.system('modprobe w1-therm')

        self.base_dir = '/sys/bus/w1/devices/'
        self.device_folder = glob.glob(self.base_dir + '28*')[0]
        self.device_file = self.device_folder + '/w1_slave'

    def read_temp(self):
#----------ファイル内容取得
        self.catdata = subprocess.Popen(['cat',self.device_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out,err = self.catdata.communicate()
        self.out_decode = out.decode('utf-8')
        self.lines = self.out_decode.split('\n')
#----------必要データの抜き出し
        while self.lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
#----------ファイル内容取得
        self.catdata = subprocess.Popen(['cat',self.device_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out,err = self.catdata.communicate()
        self.out_decode = out.decode('utf-8')
        self.lines = self.out_decode.split('\n')
        self.equals_pos = self.lines[1].find('t=')
        if self.equals_pos != -1:
            self.temp_string = self.lines[1][self.equals_pos+2:]
            self.temp_c = float(self.temp_string) / 1000.0
            return self.temp_c
#------------------------------------------------
if __name__ == '__main__':
    data = OneWireDataRead()
    temp_c = data.read_temp()
    print(temp_c)
