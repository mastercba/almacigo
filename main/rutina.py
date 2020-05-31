# rutina.py


from machine import Pin, I2C, PWM
from time import sleep
from . import ulcd1602




adc = Pin(36, Pin.IN, Pin.PULL_UP)                 # ADC 36
WT = Pin(25, Pin.OUT, value=1)                 # Water Tank
RG = Pin(26, Pin.OUT, value=1)                      # RieGo
MZ = Pin(27, Pin.OUT, value=1)                     # MeZcla
NT = Pin(14, Pin.OUT, value=1)                  # NuTre A&B
i2cR = I2C(-1, sda=Pin(18), scl=Pin(19), freq=400000)      # i2c Pin
lcdR = ulcd1602.LCD1602(i2cR)                 # LCD1602 OBJ
servo = PWM(Pin(12), freq = 50)                       #valve


class Riego:
    def __init__(self):
        print('start Riego....')
        rutinaRiego()

# ---------------------------------------------------------
def rutinaRiego():
    if not llenarTanque():
        print('no se pudo llenar tanque de agua')
        lcdR.puts("No Agua!..", 0, 1)
    mezclarTanqueAB()
    dosificaAB()
    mezclarON()
    vaciarBandejas()
    mezclarOFF()
    riego()
#     servo.deinit()
    
#     post()
# ---------------------------------------------------------

def llenarTanque():
    print('llenamos tanque de agua')
    lcdR.puts("Tanque....", 0, 1)
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
    lcdR.puts("Mezclar...", 0, 1)
    MZ.off()                             # MZ ON
    sleep(45)#45
    MZ.on()                             # MZ OFF

def dosificaAB():
    print('dosifica AB')
    lcdR.puts("Dosf A&B..", 0, 1)
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
    lcdR.puts("Cerrar....", 0, 1) 
    servo.duty(35)
    servo.duty(42)

def openValve():
    print('abrimos valvula')
    lcdR.puts("Abrir.....", 0, 1)
    servo.duty(80)  

def mezclarON():
    print('mezcla ON')
    MZ.off()                             # MZ ON

def mezclarOFF():
    print('mezcla OFF')
    MZ.on()                             # MZ OFF
    
def riego():
    print('riego')
    lcdR.puts("Riego.....", 0, 1)
    RG.off()                             # RG ON
    sleep(60)#60
    RG.on()                             # RG OFF    