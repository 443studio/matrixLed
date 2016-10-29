# -*- coding: utf-8 -*-
#control matrixLed 16x16 by Shift Resister(74hc595)
#2016/10/29 Ver3.1

import RPi.GPIO as GPIO
import time
import threading


loop_flag = True

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    for i in range(2,8):
        GPIO.setup(i, GPIO.OUT)
        GPIO.output(i,GPIO.LOW)

class matrixSResister:
    def __init__(self):
        self.Ct = [2,3,4]
        self.An = [5,6,7]
        self.SCK = 0
        self.RCK = 1
        self.SI = 2     #zanteitekinataisyo
        self.loop_flag = True
        self.drawList =
[[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],]

    def shift(self, PIN,PIN2):
        GPIO.output(PIN,GPIO.HIGH)
        GPIO.output(PIN,GPIO.LOW)

    def send(self, data, axis):
        for i in range(0,16):
            if ((1<<i)&data) == 0:
                GPIO.output(axis[self.SI], GPIO.LOW)
            else:
                GPIO.output(axis[self.SI], GPIO.HIGH)
            self.shift(axis[self.SCK])

    def reflect(self):
        self.shift(self.Ct[self.RCK])
        self.shift(self.An[self.RCK])

    def flashLed(self):
        ctptn = 65534
        for x in range(0,16):
            self.send(ctptn,self.Ct)
            self.send(self.drawList[x],self.An)
            self.reflect()
            time.sleep(0.000001)
            ctptn = ((ctptn-32768) << 1) +1
        if self.loop_flag == True:
            thr = threading.Thread(target= self.flashLed)
            thr.start()
        else:
            self.send(0,self.Ct)
            self.reflect()

    def pushList(self,newList):
        self.drawList = newList


dummyList = [0b0,
             0b0,
              0b11111111111110,
                        0b1000,
                       0b10000,
                      0b100000,
                   0b101000000,
                   0b110000000,
                   0b100000000,
                   0b100000000,
                   0b100000000,
                  0b1000000000,
                  0b1000000000,
                 0b10000000000,
               0b1100000000000,
             0b0,]

try:
    setup()
    mtrLed = matrixSResister()
    mtrLed.pushList(dummyList)
    mtrLed.flashLed()
    while True:
        time.sleep(0.5)

except KeyboardInterrupt:
    mtrLed.loop_flag = False
    time.sleep(5)
    GPIO.cleanup()
