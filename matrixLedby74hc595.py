# -*- coding: utf-8 -*-
#control matrixLed 16x16 by Shift Resister(74hc595)

import RPi.GPIO as GPIO
import time
import threading

CtSCK = 1
CtRCK = 2
CtSI = 3
AnSCK = 4
AnRCK = 5
AnSI = 6
loop_flag = True

def setup():
    GPIO.setmode(GPIO.BCM)
    for i in range(1,7):
        GPIO.setup(i, GPIO.OUT)
 
def reset():
    for i in range(1,7):
        GPIO.output(i, GPIO.LOW)
 
def shift(PIN):
    GPIO.output(PIN, GPIO.HIGH)
    GPIO.output(PIN, GPIO.LOW)
 
def send_bits(data, axis):
    pin = lambda a, b: a + b
    for i in range(16):
        if ((1 << i ) & data) == 0:
            GPIO.output(pin(axis, "SI"), GPIO.LOW)
        else:
            GPIO.output(pin(axis, "SI"), GPIO.HIGH)
        shift(pin(axis, "SCK"))
    shift(pin(axis, "RCK"))
    
def flashLed(ptn):#ptn = 16x16 List
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

dummyList = [[0101010101010101],
             [1010101010101010],
             [0101010101010101],
             [1010101010101010],
             [0101010101010101],
             [1010101010101010],
             [0101010101010101],
             [1010101010101010],
             [0101010101010101],
             [1010101010101010],
             [0101010101010101],
             [1010101010101010],
             [0101010101010101],
             [1010101010101010],
             [0101010101010101],
             [1010101010101010],]
try:
    setup()
    reset()
    flashLed(dummyList)
    while True:
        sleep(1)
        
except KeyboardInterrupt:
    loop_flag = False
    reset()
    GPIO.cleanup()
