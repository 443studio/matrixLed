import RPi.GPIO as GPIO
import threading
from time import sleep

anList = [17, 2, 3, 4, 5, 6, 7, 8]  #X
ctList = [ 9,10,11,12,13,14,15,16]  #Y

LEDSIZE = 8

y = 1
n = 0

def GPIOsetup():
    GPIO.setmode(GPIO.BCM)
    for i in range(0,8):
        GPIO.setup(anList[i],GPIO.OUT)
        GPIO.setup(ctList[i],GPIO.OUT)
    for i in range(0,LEDSIZE):
        GPIO.output(anList[i],GPIO.LOW)
        GPIO.output(ctList[i],GPIO.HIGH)


class chgLed:   #change
    def __init__ (self):
        self.drawList = []
        self.timeList = []
        self.maxframe = 0
        self.nowframe = 0
        
    def getmaxframe(self,tl):   #timelist tl
        mf = -1
        for i in tl:
            mf += 1

        return mf      #maxframe mf

    def main(self):
        if self.nowframe >= self.maxframe :
            self.nowframe = 0
        else:
            self.nowframe += 1
        self.drawList = self.timeList[self.nowframe]
        a = threading.Timer(self.wait,self.main)
        a.start()
        
    def getLedPtn(self):
        return self.drawList

    def readPtn(self):
        a = raw_input(":")
        ledptnfile = open(a + ".ledptn")
        ledptn = ledptnfile.read()
        ledptnfile.close()
        exec("self.timeList = " + ledptn)
        self.maxframe = self.getmaxframe(self.timeList)

def flashLed():
    drawList = changeList.getLedPtn()
    for y in range(0,LEDSIZE):
        GPIO.output(ctList[y],GPIO.LOW)          #Anode On
        for x in range(0,LEDSIZE):
            if drawList[y][x] != 0:
                GPIO.output(anList[x],GPIO.HIGH)   #Cathode On

        for step in range(1,8): #8tone
            sleep(0.000001)
            for x in range(0,LEDSIZE):
                if drawList[y][x] == step:
                    GPIO.output(anList[x],GPIO.LOW)
        GPIO.output(ctList[y],GPIO.HIGH)
        
        for a in range(0,8):
            GPIO.output(anList[a],GPIO.LOW)

    i = threading.Thread(target = flashLed)
    i.start()


GPIOsetup()
try:
    changeList = chgLed()
    changeList.readPtn()
    changeList.wait = input()
    changeList.main()
    flashLed()
    
    while True: 
        sleep(0.001)

except KeyboardInterrupt:
    i.cancel
    a.cancel
    GPIO.cleanup()
