# almacigo.py


from machine import Pin, I2C, PWM
from time import sleep
from . import sim800
from . import ota_updater
from . import servicio
from . import ulcd1602
import machine, onewire, ds18x20, json


#display ,0 hh:mm 25.4C xxxx
#display ,1 R:!**V:closev3.9
#display ,1 R:!**V:c #ST 3.9
#display ,1 R:!  V:c  MZ 3.9


# Create new modem object on the right Pins
modem = sim800.Modem(MODEM_PWKEY_PIN    = 4,
                     MODEM_RST_PIN      = 5,
                     MODEM_POWER_ON_PIN = 23,
                     MODEM_TX_PIN       = 16,
                     MODEM_RX_PIN       = 17)


# ESP32 Pin Layout
led = Pin(2, Pin.OUT, value=0)                          # BlueLed Pin
i2c = I2C(-1, sda=Pin(18), scl=Pin(19), freq=400000)        # i2c Pin
lcd = ulcd1602.LCD1602(i2c)                             # LCD1602 OBJ
ds_pin = machine.Pin(13)                                # DS18b20 Pin
ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))    # DS18B20 OBJ
# servo = PWM(Pin(12), freq = 50)                         #valve, close
servo = PWM(Pin(12), freq = 50)

# rutinas SMS
def smsrutina():
    #15:19/OK!
    print('RT')
    lcd.puts("#RT", 9, 1)
    smsRutina = servicio.rutinaCamas()
    lcd.puts("   ", 9, 1)
    
def smsreporte():
    #21:10/21.6*C/21 Riegos/Agua0OK..!/TDS:1200/SD23Bs
    print('ST')
    lcd.puts("#ST", 9, 1)
    #data2send = []
    #data2send.append(hr[0])
    #data2send.append(':')
    #data2send[2] = hr[1]
    #data2send.append('/')
    #modem.send_sms()
    lcd.puts("   ", 9, 1)

def smsriego():
    #15:19/1-2Riegos
    print('RG')
    lcd.puts("#RG", 9, 1)
    smsriego = servicio.rutinaAguaSMS()
    lcd.puts("   ", 9, 1)

def smsnutre():
    #15:19/OK!
    print('NT')
    lcd.puts("#NT", 9, 1)
    smsriego = servicio.dosificaAB()
    lcd.puts("   ", 9, 1)

def smsmezcla():
    #15:19/OK!
    print('MZ')
    lcd.puts("#MZ", 9, 1)
    smsriego = servicio.mezclarTanqueAB()
    lcd.puts("   ", 9, 1)

def smssensores():
    #EC:1677-TDS:905-SAL:0.84-SG:1.000
    print('SR')

def smsbandejas():
    #15:19/OK!
    print('BJ')
    lcd.puts("#BJ", 9, 1)
    smsriego = servicio.vaciarBandejas()
    lcd.puts("   ", 9, 1)
    
def smswater():
    #15:19/OK!
    print('WT')
    lcd.puts("#WT", 9, 1)
    smsriego = servicio.llenarTanque()
    if not smsriego:
        print('no se pudo llenar tanque de agua')
        lcd.puts("fail", 9, 1)
        sleep(50)
    lcd.puts("    ", 9, 1)
    

codes ={
    'RT' : smsrutina,
    'ST' : smsreporte,
    'RG' : smsriego,
    'NT' : smsnutre,
    'MZ' : smsmezcla,
    'SR' : smssensores,
    'WT' : smswater,
    'BJ' : smsbandejas
    }


## Simple software WDT implementation
wdt_counter = 0

def wdt_callback():
    global wdt_counter
    wdt_counter += 1
    if (wdt_counter >= 750):#90==1min
        machine.reset()

def wdt_feed():
    global wdt_counter
    wdt_counter = 0

wdt_timer = machine.Timer(-1)
wdt_timer.init(period=1000, mode=machine.Timer.PERIODIC, callback=lambda t:wdt_callback())
## END Simple software WDT implementation


class Nursery:
    def __init__(self, cv):
        print('start...')
        lcd.puts("R:   V:", 0, 1)         #riegos
        #servo.duty(80)
        closeV = servicio.closeValve()
        #servo.deinit()
        self.cv = cv            # ver1602
        #lcd.puts("v", 12, 1)
        lcd.puts(self.cv, 13, 1)
        # Initialize the modem
        modem.initialize()
        # Connect the modem
        modem.connect(apn='internet.tigo.bo')
        print('\nModem IP address: "{}"'.format(modem.get_ip_addr()))
        # Are time&Date valid?
        modem.get_NTP_time_date()
        rx_time_date = modem.get_time_date()# read Time&Date
        print('Date = ', rx_time_date[8:16])
        rx_time = rx_time_date.split(',')[-1].split('-')[0]
        year = str(rx_time_date[8:10])
        if (year < "20"):
            sleep(20)
            #machine.soft_reset()
            #sleep(45)
            machine.reset()
        #soft reset : import sys sys.exit()
        #hard reset : import machine machine.reset()
        #       print('Get TimeDate: "{}"'.format(modem.get_NTP_time_date()))    
        modem.set_cnmi()         # Enable CMTI notification
        modem.del_smss()               # Delete all SMS msg
        modem.set_text_mode()           # SEt SMS text mode            

        # Disconnect Modem
        #modem.disconnect()
        
        process()                          # main


# ----------------------------------------------------------
def process():
    while True:
        wdt_feed()                              # reset WDT
        blink_blue_led()                              # BBL
        system_clk = modem.get_time_date() # read Time&Date
        print('Date = ', system_clk[8:16])
        sys_time = system_clk.split(',')[-1].split('-')[0]
        print('System TIME: {}'.format(sys_time))
        hr = str(sys_time.split(':')[0])
        minu = str(sys_time.split(':')[1])
        
        #if hr == "21" and minu == "00": # refresh Time&Date
            #POST data to webServer
            #newFirmware()  # CHECK/DOWNLOAD/INSTALL/REBOOT
        
                                           # time to routine
        if (hr[0] == "0" and hr[1] == "4") and minu == "30":
            lcd.puts("w", 2, 1)
            rt = servicio.rutinaRiego()
            print(rt)
            #print('temperaruta: ', rt[TP]['18b20'])
#        if hr == "12" and minu == "00":     # time to water
#            lcd.puts("w", 3, 1)
#            agua = servicio.rutinaAgua12()
#        if hr == "20" and minu == "00":     # time to water    
#            lcd.puts("w", 4, 1)
#            agua1 = servicio.rutinaAgua20() 

        sms_rqst = modem.check_sms_rcv()       # data rcved
        vals = list(sms_rqst.values())
        if vals[1] != '0':
            work = codes[vals[0]]
            work()
                                                   # mezcla
        if int(hr) in range(10,23,3) and (minu == "00"):
            mz = servicio.mezclarTanqueAB()

        print_date_time()               # LCD1602 date&time
        ds18b20()                    # read&LCD1602 ds18b20
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
    system_clk = modem.get_time_date()  # read Time&Date
    print('Date = ', system_clk[8:16])
    sys_time = system_clk.split(',')[-1].split('-')[0]
    print('System TIME: {}'.format(sys_time))
    hr = str(sys_time.split(':')[0])
    minu = str(sys_time.split(':')[1])
    lcd.puts(":", 2, 0)     #:
    lcd.puts(hr, 0, 0)      #hora
    lcd.puts(minu, 3, 0)    #minute

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
    