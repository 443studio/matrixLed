# -*- coding: utf-8 -*-
#control matrixLed 16x16 by Shift Resister(74hc595)
#2016/10/25 Ver2.0

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
        
def shift(PIN):
    GPIO.output(PIN,GPIO.HIGH)
    GPIO.output(PIN,GPIO.LOW)
    
def send(data, axis):
    pin = lambda a, b: a + b
    for i in range(16):
        if ((1 << i ) & data) == 0:
            GPIO.output(pin(axis, "SI"), GPIO.LOW)
        else:
            GPIO.output(pin(axis, "SI"), GPIO.HIGH)
        shift(pin(axis, "SCK"))
        
def reflect():
    shift(An_RCK)
    shift(Ct_RCK)
    
def flashLed():#ptn = 16x16 List
    ptn = dummyList #暫定的な対処
    reset()
    ct = 1
    for x in range(0,16):
        send_bits(ct,"Ct")
        send_bits(ptn[x])
        for i in range(0,100):#
            if True:          #テスト用wait
                pass          #
        ct = ct << 1
    if loop_flag == True:
        threading.Thread(target=flashLed)
    else:
        send_bits(0)

try:
    setup()
    flashLed(dummyList)
    while True:
        time.sleep(1)
        
except KeyboardInterrupt:
    loop_flag = False
    reset()
    GPIO.cleanup()
