#! /usr/bin/env python3
# coding: UTF-8
#CRC8の計算
#2019.01.28 by SGR

class CrcCalc(object):

    def __init__(self, polynominal):
        """CRC多項式を引数にオブジェクトを生成"""
        self._poly = polynominal

    def crc_dat(self, _data):
        """dataからcrcの値を計算して返す"""
        #---- 処理するデータ列のＢｉｔ長を取得
        self._length    = len(bin(_data)[2:]) #dataをstrに変換して上位２つを削除→基数の0bを消す
        #---- 多項式データ列のＢｉｔ長を取得
        self._leng_poly = len(bin(self._poly)[2:]) #polyをstrに変換して上位２つを削除→基数の0bを消す
        #-------CRC演算
        while self._length >= self._leng_poly: #多項式のBit長よりもデータが短くなるまで演算を繰り返す。終わって残ったものがCRC
            _data = _data ^ (self._poly << (self._length - self._leng_poly)) #polyをdataの先頭にアライメントしてXOR
            self._length = len(bin(_data)[2:]) #dataをstrに変換して上位２つを削除→基数0b削除して長さを返す
        #---答え
        return _data


#-----------------------------------------------
if __name__ == "__main__":
    crc8atm = CrcCalc(0b100000111)

    crc8data = crc8atm.crc_dat(0x65432100)
    print("\n","crc8atm =",hex(crc8data))
