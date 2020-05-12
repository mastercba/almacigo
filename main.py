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

    ota_updater = OTAUpdater('https://github.com/mastercba/almacigo')
    ota_updater.using_network('TORRIMORA', 'santino989')
    ota_updater.check_for_update_to_install_during_next_reboot()    

    #INIT time&date
    date = MyTimeDate()

    
    #Begin MAINcode
    seed = Nursery()

def boot():
    download_and_install_update_if_available()
    start()
    

boot()
# -----------------------------------------------------------------------------
