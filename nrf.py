#!/usr/bin/env python

from time import sleep
import RPi.GPIO as GPIO
import time
import json
from websocket import create_connection

#Initialize GPIO Pins(21,23,24,25,26,27)
#Number Photocells(Order based on orientation on Board)
photocell1=26
photocell2=17
photocell3=13
photocell4=19
photocell5=22
photocell6=27

#Set GPIO Mode to BCM (On board pins)
GPIO.setmode(GPIO.BCM)

#Set Mode to input
GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#Set GPIO Warnings to False
#GPIO.setwarnings(False)

#Product Timers Initilizations
prdtimer1=0
prdtimer2=0
prdtimer3=0
prdtimer4=0
prdtimer5=0
prdtimer6=0

#Product Timer Array(For AVG Calculation)
prdarr1=[]
prdarr2=[]
prdarr3=[]
prdarr4=[]
prdarr5=[]
prdarr6=[]

#Pickup Boolean Values
pickup1=0

#Average Variables
prdavg1=0
prdavg2=0
prdavg3=0
prdavg4=0
prdavg5=0
prdavg6=0

#Setup Websocket ws Var
ws = "global"

#Setup Websocket Connection
def connectWebsocket():
    try:
        global ws 
        ws = create_connection("wss://mgwws.hana.ondemand.com/endpoints/v1/ws")
    except:
        print("Error connecting to Websocket")

def PickedUp(prd):
    #Start Local Prd Timer
    prd=time.time()
    pickup1=1
    print("Pickup Product")
    #Return Initial Start Value
    return prd

def PutDown(prd,prdarr):
    #Calculate Time Picked Up
    endtime = time.time()
    prd=endtime-prd
    return prd
    #Set Pickup Var to 0=>Put Down
    pickup1=0
    #Append to Timer Array for AVG Calc
    #Reset Timer
    prd=0

def calculateAvgArray(array,num):
    sum = 0
    for i in range(num):
        sum += array[i]
    return round(sum/num);

def send_data(color,present,avg):
    data = json.dumps({"topic": "in/nait/nrf/shelf", "color": color, "present": present, "time": avg})
    ws.send(data)
    #result = ws.recv()

#Initialize Websocket Connection
connectWebsocket()
websocketReset = 0

#Value to denote if product is on or off (0=off,1=on)
shelfVal = 1

#Counter to initiate on/off
counter1 = 0

#Store Last Lifted Product
lastLifted = 0


#Initialize Infinite Loop
while True:
    time.sleep(0.05)
    if (GPIO.input(photocell1)==shelfVal):
        if (counter1 < 1):
            print("Product Removed [1]")
            prdtimer1 = PickedUp(prdtimer1)
            lastLifted=1
            send_data("millennialpink","no",prdavg1)
            counter1 = 1
    elif (GPIO.input(photocell2)==shelfVal):
        if (counter1 < 1):
            print("Product Removed [2]")
            prdtimer2 = PickedUp(prdtimer2)
            lastLifted=2
            send_data("plumepink","no",prdavg2)
            counter1 = 1 
    elif(GPIO.input(photocell3)==shelfVal):
        if (counter1 < 1):
            print("Removed From 3")
            prdtimer3 = PickedUp(prdtimer3)
            lastLifted=3
            send_data("saltedcaramel","no",prdavg3)
            counter1 = 1
    elif(GPIO.input(photocell4)==shelfVal):
        if (counter1 < 1):
            print("Removed From 4")
            prdtimer4 = PickedUp(prdtimer4)
            lastLifted=4
            send_data("satinglow","no",prdavg4)
            counter1 = 1
    elif(GPIO.input(photocell5)==shelfVal):
        if (counter1 < 1):
            print("Removed From 5")
            prdtimer5 = PickedUp(prdtimer5)
            lastLifted=5
            send_data("suavemauve","no",prdavg5)
            counter1 = 1
    elif(GPIO.input(photocell6)==shelfVal):
        if (counter1 < 1):
            print("Removed From 6")
            prdtimer6 = PickedUp(prdtimer6)
            lastLifted = 6
            send_data("trulytangerine","no",prdavg6)
            counter1 = 1
    else:
        if(counter1 == 1):
            if (lastLifted == 1):
                print "Product Placed Back"
                prdarr1.append(PutDown(prdtimer1,prdarr1))
                PickedUpCount1 = len(prdarr1)
                prdavg1 = calculateAvgArray(prdarr1,PickedUpCount1)
                print prdavg1
                send_data("millennialpink","yes",prdavg1)
                print prdarr1
            elif (lastLifted == 2):
                print "Product Placed Back"
                prdarr2.append(PutDown(prdtimer2,prdarr2))
                PickedUpCount2 = len(prdarr2)
                prdavg2 = calculateAvgArray(prdarr2,PickedUpCount2)
                send_data("plumepink","yes",prdavg2)
                print prdarr2
            elif (lastLifted == 3):
                print "Product Placed Back"
                prdarr3.append(PutDown(prdtimer3,prdarr3))
                PickedUpCount3 = len(prdarr3)
                prdavg3 = calculateAvgArray(prdarr3,PickedUpCount3)
                send_data("saltedcaramel","yes",prdavg3)
                print prdarr3
            elif (lastLifted == 4):
                print "Product Placed Back"
                prdarr4.append(PutDown(prdtimer4,prdarr4))
                PickedUpCount4 = len(prdarr4)
                prdavg4 = calculateAvgArray(prdarr4,PickedUpCount4)
                send_data("satinglow","yes",prdavg4)
                print prdarr4
            elif (lastLifted == 5):
                print "Product Placed Back"
                prdarr5.append(PutDown(prdtimer5,prdarr5))
                PickedUpCount5 = len(prdarr5)
                prdavg5 = calculateAvgArray(prdarr5,PickedUpCount5)
                send_data("suavemauve","yes",prdavg5)
                print prdarr5
            elif (lastLifted==6):
                print "Product Placed Back"
                prdarr6.append(PutDown(prdtimer6,prdarr6))
                PickedUpCount6 = len(prdarr6)
                prdavg6 = calculateAvgArray(prdarr6,PickedUpCount6)
                send_data("trulytangerine","yes",prdavg6)
                print prdarr6
            counter1 = 0
            
    #Reset Websocket Every Minute if WiFi is lost
    websocketReset+=1
    if (websocketReset==400000):
        print ("Resetting Websocket")
        connectWebsocket()
        websocketReset=0
