# almacigo.py


from machine import Pin, I2C
from time import sleep


#ESP32 BlueLed Pin
led = Pin(13, Pin.OUT, value=0) #BlueLed Pin


class Nursery:
    def __init__(self):
        print('start NURSERY')
        process()


#------------------------------------------------       
def process():
    while True:
        blink_blue_led()
    

#------------------------------------------------        

#BlinkBlueLed
def blink_blue_led():
    led.value(1)
    sleep(0.1)
    led.value(0)
    sleep(5.0)        
        
