# MAIN - SEEDING v0.1.0 r1.2
# -----------------------------------------------------------------------------

from main.ota_updater import OTAUpdater 
from main import almacigo


def download_and_install_update_if_available():
    ota_updater = OTAUpdater('https://github.com/mastercba/almacigo')
    ota_updater.download_and_install_update_if_available('TORRIMORA', 'santino989')

def start():
    from main import ota_updater
    from main.almacigo import Nursery

    ota_updater = OTAUpdater('https://github.com/mastercba/almacigo')
#    ota_updater.download_and_install_update_if_available('TORRIMORA', 'santino989')
    ota_updater.using_network('TORRIMORA', 'santino989')
    ota_updater.check_for_update_to_install_during_next_reboot()    
    seed = Nursery()

def boot():
    download_and_install_update_if_available()
    start()
    

boot()
# -----------------------------------------------------------------------------
