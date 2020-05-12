# almacigo.py


from machine import Pin, I2C
from time import sleep
from . import time_date
from . import ota_updater


#ESP32 BlueLed Pin
led = Pin(13, Pin.OUT, value=0) #BlueLed Pin


class Nursery:
    def __init__(self):
        print('start NURSERY')
        process()


#----------------------------------------------------------       
def process():
    while True:
        blink_blue_led()                               #BBL
        date = time_date.MyTimeDate()       #read Time&Date
        dt = date.readTimeDate()
        print(dt[0],":",dt[1],"/",dt[2],"/",dt[3],"/",dt[4])
        if dt[0] == 21 and dt[1]==00:     #refresh Time&Date
            date = time_date.MyTimeDate()
            dt = date.readTimeDate()
            newFirmware()    #CHECK/DOWNLOAD/INSTALL/REBOOT
            
#----------------------------------------------------------        

#BlinkBlueLed
def blink_blue_led():
    led.value(1)
    sleep(0.1)
    led.value(0)
    sleep(5.0)

#NewUPdate2install?
def newFirmware():
    from main import ota_updater
    ota_updater = ota_updater.OTAUpdater('https://github.com/mastercba/almacigo')
    ota_updater.download_and_install_update_if_available('TORRIMORA', 'santino989')
    ota_updater.check_for_update_to_install_during_next_reboot()   
