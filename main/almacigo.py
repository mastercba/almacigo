# almacigo.py


from machine import Pin, I2C
from time import sleep
from . import time_date
from . import ota_updater
from . import rutina
from . import ulcd1602


# ESP32 Pin Layout
led = Pin(13, Pin.OUT, value=0)         # BlueLed Pin
i2c = I2C(1, sda=Pin(21), scl=Pin(22))  # i2c Pin
lcd = ulcd1602.LCD1602(i2c)             # LCD1602 OBJ

class Nursery:
    def __init__(self, cv):
        print('start...')
        self.cv = cv            # ver1602
        lcd.puts("v", 12, 1)
        lcd.puts(self.cv, 13, 1)
        process()               # main


# ----------------------------------------------------------
def process():
    while True:
        blink_blue_led()                              # BBL
        date = time_date.MyTimeDate()      # read Time&Date
        dt = date.readTimeDate()
        if dt[0] == 21 and dt[1] == 0:  # refresh Time&Date
            date = time_date.MyTimeDate()
            dt = date.readTimeDate()
            newFirmware()   # CHECK/DOWNLOAD/INSTALL/REBOOT
        if dt[0] == 4 and dt[1] == 30:
            rt = rutina.Riego()
        print_date_time()               # LCD1602 date&time

# ----------------------------------------------------------

# BlinkBlueLed
def blink_blue_led():
    led.value(1)
    sleep(0.1)
    led.value(0)
    sleep(5.0)

# NewUPdate2install?
def newFirmware():
    from main import ota_updater
    ota_updater = ota_updater.OTAUpdater('https://github.com/mastercba/almacigo')
    ota_updater.download_and_install_update_if_available('TORRIMORA', 'santino989')
    ota_updater.check_for_update_to_install_during_next_reboot()   

# LCD1602 date&time
def print_date_time():
    date = time_date.MyTimeDate()      # read Time&Date
    dt = date.readTimeDate()
    if dt[1] < 10:
        lcd.puts(dt[0], 0, 0)
        lcd.puts(":", 2, 0)
        lcd.puts("0", 3, 0)
        lcd.puts(dt[1], 4, 0)
    elif dt[0] < 10:
        lcd.puts("0", 0, 0)
        lcd.puts(dt[0], 1, 0)
        lcd.puts(":", 2, 0)
        lcd.puts(dt[1], 3, 0)
    else:
        lcd.puts(dt[0], 0, 0)
        lcd.puts(":", 2, 0)
        lcd.puts(dt[1], 3, 0)