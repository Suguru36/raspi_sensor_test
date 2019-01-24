#!/usr/bin/env python
import smbus
import time
i2c = smbus.SMBus(1)
addr = 0x5a

def crc8atm(data) : #data=0x654321
        data =data <<8
#        print(hex(data),"data")
        length = len(bin(data)[2:])
        for i in range(length):
                if int(bin(data)[2:3],2) == 1 : #MSB =1
                        nokori = bin(data)[11:]
                        sentou = (int(bin(data)[2:11],2)) ^ (int('100000111',2))
                        data = int((str(bin(sentou)[2:11])+str(nokori)),2)
                data=int(bin(data),2)
                if len(str(bin(data)[2:]))<9:
                        return(hex(data))
#main
#i2c.write_i2c_block_data(addr,0x25,[0xb4,0x9f,0x8c]) #default
#i2c.write_i2c_block_data(addr,0x25,[0xb4,0xcf,0x3b]) #gain=25
print(bin(i2c.read_word_data(addr,0x22)) ,"PWMCTRL")
print(bin(i2c.read_word_data(addr,0x25)) ,"Config Register1")
print(hex(i2c.read_byte_data(addr,0x2e)) ,"slave address")
time.sleep(0.5)
while 1:
        Atemp = i2c.read_i2c_block_data(addr,0x6,3)
        Otemp1 = i2c.read_i2c_block_data(addr,0x7,3)
#        Otemp2 = i2c.read_i2c_block_data(addr,0x8,3)
        AmbientTemp = ((Atemp[1]*256 + Atemp[0]) *0.02 -273.15)
        ObjectTemp1 = ((Otemp1[1]*256 + Otemp1[0]) *0.02 -273.15)
#        ObjectTemp2 = ((Otemp2[1]*256 + Otemp2[0]) *0.02 -273.15)
        print(round(AmbientTemp,2),round(ObjectTemp1,2))#,round(ObjectTemp2,2))
        print("TempHEXAdata",hex(Atemp[0]),hex(Atemp[1]))
        print(hex(Atemp[2]),bin(Atemp[2]),"<-readedCRC")
        #(slaveAdress+W)+(書き込みアドレス)+(slaveAdress+R)+(ReadData1)+(ReadData2)を文字列に整形したものをcrc8atmへ渡す
        data1 = int(crc8atm(int(("b406b5"+str(hex(Atemp[0])[2:]).zfill(2)+str(hex(Atemp[1])[2:]).zfill(2)),16)),16)
        print(hex(data1), bin(data1), "<-calculated")
        time.sleep(1)
