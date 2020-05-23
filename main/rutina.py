# rutina.py


from machine import Pin, I2C, PWM
from time import sleep

rutina = {
    "tanque": False,
    "mezclar": False,
    "dosificar": False,
    "vaciar": False,
    "riego": False,
    "post": False,
    }


adc = Pin(36, Pin.IN, Pin.PULL_UP)                 # ADC 36
WT = Pin(33, Pin.OUT, value=1)                 # Water Tank
RG = Pin(32, Pin.OUT, value=1)                      # RieGo
MZ = Pin(25, Pin.OUT, value=1)                     # MeZcla
NT = Pin(14, Pin.OUT, value=1)                  # NuTre A&B


class Riego:
    def __init__(self):
        print('start Riego....')
        rutinaRiego()

# ---------------------------------------------------------
def rutinaRiego():
    if not llenarTanque():
        print('no se pudo llenar tanque de agua')
    mezclarTanqueAB()
    dosificaAB()
    mezclarON()
    vaciarBandejas()
    mezclarOFF()
    riego()
#     post()
# ---------------------------------------------------------

def llenarTanque():
    print('llenamos tanque de agua')
    dog = 1
    num = 0
    WT.off()
    MZ.off()
    while adc.value() == 1:            # 1:vacio
        print("{}vacio".format(adc.value()))
        dog = dog + 1
        print(dog)
        sleep(2) #2
        if dog == 50:
            if num == 2:
                print('FAIL!')
                return False       #tanque vacio
            num=num+1
            dog=1
            WT.on()
            MZ.on()
            sleep(10)
            WT.off()
            MZ.off()
    WT.on()
    MZ.on()
    return True                    #tanque lleno

def mezclarTanqueAB():
    print('mezclar tanques')
    MZ.off()                             # MZ ON
    sleep(45)#45
    MZ.on()                             # MZ OFF

def dosificaAB():
    print('dosifica AB')
    NT.off()                             # NT ON
    sleep(8)#8
    NT.on()                             # NT OFF

def vaciarBandejas():
    #Close Valve
    openValve()
    #wait....
    sleep(90)#90
    #Open Valve
    closeValve()
    
def closeValve():
    print('cerramos valvula')
    servo = PWM(Pin(2), freq = 50)
    servo.duty(40)
    servo.deinit()

def openValve():
    print('abrimos valvula')
    servo = PWM(Pin(2), freq = 50)
    servo.duty(80)
    servo.deinit()

def mezclarON():
    print('mezcla ON')
    MZ.off()                             # MZ ON

def mezclarOFF():
    print('mezcla OFF')
    MZ.on()                             # MZ OFF
    
def riego():
    print('riego')
    RG.off()                             # RG ON
    sleep(60)#60
    RG.on()                             # RG OFF    