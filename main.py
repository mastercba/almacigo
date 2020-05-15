# MAIN - SEEDING
# -----------------------------------------------------------------------------

from main.ota_updater import OTAUpdater 
from main import almacigo


def download_and_install_update_if_available():
    ota_updater = OTAUpdater('https://github.com/mastercba/almacigo')
    ota_updater.download_and_install_update_if_available('TORRIMORA', 'santino989')

def start():
    from main import ota_updater
    from main import time_date
    from main.almacigo import Nursery
    from main.time_date import MyTimeDate
    from main.ulcd1602 import LCD1602
    from machine import Pin, I2C

    ota_updater = OTAUpdater('https://github.com/mastercba/almacigo')
    ota_updater.using_network('TORRIMORA', 'santino989')
    ota_updater.check_for_update_to_install_during_next_reboot()

    # LCD1602 version
    cv = ota_updater.read_current_version()
    i2c = I2C(1, sda=Pin(21), scl=Pin(22))
    lcd = LCD1602(i2c)  # print LCD1602
    lcd.puts(cv, 10, 1)

    # INIT time&date
    date = MyTimeDate()
    dt = date.readTimeDate()
    
    # Begin MAINcode
    seed = Nursery()

def boot():
    download_and_install_update_if_available()
    start()
    

boot()
# -----------------------------------------------------------------------------
