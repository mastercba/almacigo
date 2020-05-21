# rutina.py


from machine import Pin, I2C, PWM

servo = PWM(Pin(2), freq = 50)


class Riego:
    def __init__(self):
        print('start Riego')
        rutinaRiego()

# ---------------------------------------------------------
def rutinaRiego():
    llenarTanque()
    mezclarTanqueAB()
    dosificaAB()
    mezclarON()
    mezclarOFF()

# ---------------------------------------------------------

def closeValve():
    print('cerramos valvula')
    servo.duty(45)

def openValve():
    print('abrimos valvula')
    servo.duty(80)
    
def llenarTanque():
    print('llenamos tanque de agua')

def mezclarTanqueAB():
    print('mezclar tanques')

def dosificaAB():
    print('dosifica AB')

def mezclarON():
    print('mezcla ON')