# water_quality.py


from machine import Pin, I2C
from time import sleep
from . import ulcd1602


i2cWQ = I2C(-1, sda=Pin(18), scl=Pin(19), freq=400000)# i2c Pin
lcdWQ = ulcd1602.LCD1602(i2cWQ)                   # LCD1602 OBJ

# ---------------------------------------------------------
def set_K_wqs():
    lcdWQ.puts("     ", 11, 0)
    lcdWQ.puts("largo", 11, 0)
    output = i2cWQ.writeto(100, b'K,0.1')     #K1.0(corto)
    sleep(2.0)                                #K0.1(largo)
# ---------------------------------------------------------
def set_params_wqs():
    i2cWQ.writeto(100, b'O,TDS,1')
    sleep(2)
    i2cWQ.writeto(100, b'O,S,1')
    sleep(2)
    i2cWQ.writeto(100, b'O,SG,1')
    sleep(2)
# ---------------------------------------------------------
def read_wqs():
    i2cWQ.writeto(100, b'r')
    sleep(2)
    rcv = i2cWQ.readfrom(100, 21)
    print(rcv)
    r = rcv.split(b',')
    print(r)
    #print('EC  :{} '.format(r[0].decode("ascii")))
    #print('TDS :{} '.format(r[1].decode("ascii")))
    #print('SAL :{} '.format(r[2].decode("ascii")))
    #print('SG  :{} '.format(r[3].decode("ascii")))
    tds = r[1].decode("ascii")
    lcdWQ.puts("     ", 11, 0)
    lcdWQ.puts(tds, 12, 0)
# ---------------------------------------------------------