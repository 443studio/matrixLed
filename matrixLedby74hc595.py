# -*- coding: utf-8 -*-
#control matrixLed 16x16 by Shift Resister(74hc595)
#2016/10/25 Ver3.0

import RPi.GPIO as GPIO
import time
import threading

Ct_SCK = 1
Ct_RCK = 2
Ct_SI  = 3
An_SCK = 4
An_RCK = 5
An_SI  = 6
loop_flag = True

def setup():
    GPIO.setmode(GPIO.BCM)
    for i in range(1,7):
        GPIO.setup(i, GPIO.OUT)
    for i in range(1,7):
        GPIO.output(i,GPIO.LOW)

class matrixSResister:
    def __init__(self):
        self.drawList = []

    def shift(self, PIN):
        GPIO.output(PIN,GPIO.HIGH)
        GPIO.output(PIN,GPIO.LOW)
    
    def send(self, data, axis):
        pin = lambda a, b: a + b
        for i in range(16):
            if ((1 << i ) & data) == 0:
                GPIO.output(pin(axis, "SI"), GPIO.LOW)
            else:
                GPIO.output(pin(axis, "SI"), GPIO.HIGH)
            shift(pin(axis, "SCK"))

    def reflect(self):
        shift(An_RCK)
        shift(Ct_RCK)

    def flashLed(self,name):
    reset()
    ct = 1
    for x in range(0,16):
        send_bits(ct,"Ct")
        send_bits(self.drawList[x],"An")
        reflect()
        time.sleep(0.000001)
        ct = ct << 1
    if loop_flag == True:
        threading.Thread(target= name+"flashLed")
    else:
        send_bits(0)
        reflect()

dummyList = [[21845],
             [43690],
             [21845],
             [43690],
             [21845],
             [43690],
             [21845],
             [43690],
             [21845],
             [43690],
             [21845],
             [43690],
             [21845],
             [43690],
             [21845],
             [43690],]

try:
    setup()
    mtrLed = matrixSResiter()
    mtrLed.drawList = dummyList
    mtrLed.flashLed()
    while True:
        sleep(0.5)

except KeyboardInterrupt:
    loop_flag = False
    GPIO.cleanup()
