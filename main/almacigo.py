# almacigo.py


from machine import Pin, I2C, PWM
from time import sleep
from . import time_date
from . import ota_updater
from . import rutina
from . import ulcd1602
import machine, onewire, ds18x20


# ESP32 Pin Layout
led = Pin(2, Pin.OUT, value=0)                          # BlueLed Pin
i2c = I2C(-1, sda=Pin(18), scl=Pin(19), freq=400000)        # i2c Pin
lcd = ulcd1602.LCD1602(i2c)                             # LCD1602 OBJ
ds_pin = machine.Pin(13)                                # DS18b20 Pin
ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))    # DS18B20 OBJ
# servo = PWM(Pin(12), freq = 50)                         #valve, close



class Nursery:
    def __init__(self, cv):
        print('start...')
        #servo.duty(80)
        closeV = rutina.closeValve()
        lcd.puts("          ", 0, 1)
        #servo.deinit()
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
#             newFirmware()   # CHECK/DOWNLOAD/INSTALL/REBOOT
            lcd.puts("          ", 0, 1)
            lcd.puts("    ", 12, 0)
        if dt[0] == 4 and dt[1] == 30:    # time to routine
            lcd.puts("Working..", 0, 1) 
            rt = rutina.Riego()
            lcd.puts("Done!     ", 0, 1)
            date = time_date.MyTimeDate()
            dt = date.readTimeDate()
            lcd.puts(dt[0], 12, 0)      #hour
            lcd.puts(":", 13, 0)        #:
            if dt[1] < 10:              #minute
                lcd.puts("0", 14, 0)
                lcd.puts(dt[1], 15, 0)
            else:
                lcd.puts(dt[1], 14, 0)
        print_date_time()               # LCD1602 date&time
        ds18b20()                    # read&LCD1602 ds18b20
#         servo = PWM(Pin(2), freq = 50, duty = 40)
#         waterQuality()              # set K0.1 waterquality
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

# DS18B20
def ds18b20():
    roms = ds_sensor.scan()
    #print('Found DS devices: ', roms)
    ds_sensor.convert_temp()
    #time.sleep_ms(750)
    for rom in roms:
      temp = ("%.1f" % round(ds_sensor.read_temp(rom), 1))  
      #print(rom)
      #print("%.1f" % round(temp, 2))
      #print("/")
      #print(round(temp, 1))
      #print(ds_sensor.read_temp(rom))
    #time.sleep(5)
      lcd.puts(temp, 6, 0)   # ds18b20->lcd1602
      lcd.puts("C", 10, 0)

# Water Quality Sensor
# def waterQuality():
#     i2c.writeto(100, b'K,0.1')
#     sleep(5.0)
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
    