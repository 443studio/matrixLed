import RPi.GPIO as GPIO
from time import *
import threading

anList = [17, 2, 3, 4, 5, 6, 7, 8]  #X
ctList = [ 9,10,11,12,13,14,15,16]  #Y

LEDSIZE = 8

y = 1
n = 0



def GPIOsetup():                             #OK
    GPIO.setmode(GPIO.BCM)
    for i in range(0,8):
        
        GPIO.setup(anList[i],GPIO.OUT)
        GPIO.setup(ctList[i],GPIO.OUT)
    for i in range(0,LEDSIZE):
        GPIO.output(anList[i],GPIO.LOW)
        GPIO.output(ctList[i],GPIO.HIGH)
        

def setLed(List):
    x = input("x:")
    y = input("y:")
    s = input("s:")
    List[x][y] = s
    return List


def setLedAll(List,s):
    for x in range(0,8):
        for y in range(0,8):
            List[x][y] =  s 
    return s


        
def flashLed():
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
    global i

def moveLedptn(ptnfile, ne):
    global drawList
    for i in range(0,ne):
        drawList = ptnfile[i]
        sleep(0.07)

def readPtnfile():
    a = raw_input(":")
    ledptnfile = open(a + ".ledptn")
    ledptn = ledptnfile.read()
    ledptnfile.close()
    exec("List = " + ledptn)
    return List

def countList(ptnfile):
    a = 0
    for i in ptnfile:
        a += 1
    return a
########################################
    
drawList =[
     [0,0,0,0,0,0,0,0,],
     [0,0,0,0,0,0,0,0,],
     [0,0,0,0,0,0,0,0,],
     [0,0,0,0,0,0,0,0,],
     [0,0,0,0,0,0,0,0,],    #dummy
     [0,0,0,0,0,0,0,0,],
     [0,0,0,0,0,0,0,0,],
     [0,0,0,0,0,0,0,0,],
    ]
ptnfile = []
List = []

GPIOsetup()


try:
    ptnfile = readPtnfile()
    ne = countList(ptnfile)                      #number of element

    flashLed()

    while True:
        moveLedptn(ptnfile, ne)
except KeyboardInterrupt:
    i.cancel()
    GPIO.cleanup()
