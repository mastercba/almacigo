# water_quality.py


from machine import Pin, I2C
from time import sleep
from . import ulcd1602


i2cWQ = I2C(-1, sda=Pin(18), scl=Pin(19), freq=400000)# i2c Pin
lcdWQ = ulcd1602.LCD1602(i2cWQ)                   # LCD1602 OBJ


# ---------------------------------------------------------
# Water Quality Sensor ------------------------------------

def setk():
    output = i2cWQ.writeto(100, b'K,0.1')
    sleep(5.0)
    print(output)
    
#     code = 0
#     while  not(code == 1):
#         i2c.start()
#         i2c.writeto(100, b'r')
#         sleep(1.0)
#         code = ord(i2c.readfrom(100, 1))
#         print(code)
#     sleep(15.0)    
#     print('WQS data is ready!')
#     wqs_buffer = i2c.readfrom(100, 48)
#     i2c.stop()
#     print(wqs_buffer)

# ---------------------------------------------------------