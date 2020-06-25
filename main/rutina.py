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
        lcdR.puts("!", 2, 1)
        return
    mezclarTanqueAB()
    dosificaAB()
    mezclarON()
    vaciarBandejas()
    mezclarOFF()
    riego()
    lcdR.puts("*", 2, 1)
# ---------------------------------------------------------
def rutinaAgua12():
    if not llenarTanque():
        print('no se pudo llenar tanque de agua')
        lcdR.puts("!", 3, 1)
        return
    lcdR.puts("m", 3, 1)
    mezclarTanqueAB()
    lcdR.puts("r", 3, 1)
    riego()
    lcdR.puts("*", 3, 1)
# ---------------------------------------------------------
def rutinaAgua20():
    if not llenarTanque():
        print('no se pudo llenar tanque de agua')
        lcdR.puts("!", 4, 1)
        return
    lcdR.puts("m", 4, 1)
    mezclarTanqueAB()
    lcdR.puts("r", 4, 1)
    riego()
    lcdR.puts("*", 4, 1)
# ---------------------------------------------------------
def rutinaAguaSMS():
    if not llenarTanque():
        print('no se pudo llenar tanque de agua')
        return
    mezclarTanqueAB()
    riego()
# ---------------------------------------------------------
def llenarTanque():
    print('llenamos tanque de agua')
    dog = 1
    num = 0
    WT.off()
    sleep(2)
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
    sleep(2)
    MZ.on()
    sleep(2)
    return True                    #tanque lleno

def mezclarTanqueAB():
    print('mezclar tanques')
    lcd.puts("MZ", 10, 1)
    MZ.off()                             # MZ ON
    sleep(120)# en segundos
    MZ.on()                             # MZ OFF
    lcd.puts("  ", 10, 1)

def dosificaAB():
    print('dosifica AB')
    NT.off()                             # NT ON
    sleep(17)# en segundos
    NT.on()                             # NT OFF

def vaciarBandejas():
    #Close Valve
    openValve()
    #wait....
    sleep(240)# en segundos
    #Open Valve
    closeValve()
    
def closeValve():
    print('cerramos valvula')
    lcdR.puts(" ", 7, 1)
    servo.duty(35)
    servo.duty(42)
    lcdR.puts("c", 7, 1)

def openValve():
    print('abrimos valvula')
    lcdR.puts(" ", 7, 1)
    servo.duty(80)
    lcdR.puts("o", 7, 1)

def mezclarON():
    print('mezcla ON')
    MZ.off()                             # MZ ON

def mezclarOFF():
    print('mezcla OFF')
    MZ.on()                             # MZ OFF
    
def riego():
    print('riego')
    RG.off()                             # RG ON
    sleep(270)#90=1minuto
    RG.on()                             # RG OFF