#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import cv2
import os

from libraryCH.device.camera import PICamera
from libraryCH.device.lcd import ILI9341

lcd = ILI9341(LCD_size_w=240, LCD_size_h=320, LCD_Rotate=270)

numInput = raw_input("Please enter your gesture number: ")

def wait():
    raw_input('Press Enter')

def createFolder(pathFolder):
    if(not os.path.exists(pathFolder)):
        os.makedirs(pathFolder)

def writeImage(num, img):
    global imgFolder
    imgFile = ("G{}.png".format(num))
    cv2.imwrite(imgFolder + imgFile, img)

imgFolder = ("imgGesture/{}/".format(numInput))
print ("Images will save to: {}".format(imgFolder))
if(not numInput==""):  createFolder(imgFolder)

cap = cv2.VideoCapture(0)

k=np.ones((3,3),np.uint8)

t0 = cap.read()[1]
t1 = cap.read()[1]

i = 0
while(True):
    grey1 = cv2.cvtColor(t0, cv2.COLOR_BGR2GRAY)
    grey2 = cv2.cvtColor(t1, cv2.COLOR_BGR2GRAY)
    blur1 = cv2.GaussianBlur(grey1,(7,7),0)
    blur2 = cv2.GaussianBlur(grey2,(7,7),0)

    d=cv2.absdiff(blur1,blur2)
    ret, th = cv2.threshold( d, 15, 255, cv2.THRESH_BINARY )
    dilated=cv2.dilate(th,k,iterations=2)
    canny = cv2.Canny(dilated, 50, 150) 
    contours, hierarchy = cv2.findContours(canny,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    t2=t0
    cv2.drawContours(t2, contours, -1, (0,255,0), 2 )
    lcd.displayImg(t2)
    if(not numInput==""): writeImage(i, canny)
    #print("dilated.shape={}".format(dilated.shape))

    t0=t1
    t1=cap.read()[1]    

    if cv2.waitKey(5) == 27 :
        break

    i = i + 1

cap.release()
