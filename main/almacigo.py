# almacigo.py  v0.1.2 r1.2



from machine import Pin, I2C
from time import sleep


#ESP32 BlueLed Pin
led = Pin(13, Pin.OUT, value=0) #BlueLed Pin


class Nursery:
    def __init__(self):
        print('start NURSERY v0.1.2 r1.2')
        process()


#------------------------------------------------       
def process():
    while True:
        blink_blue_led()
    

#------------------------------------------------        

#BlinkBlueLed r1.2
def blink_blue_led():
    led.value(1)
    sleep(0.1)
    led.value(0)
    sleep(5.0)        
        
