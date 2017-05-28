#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import cv2

from libraryCH.device.camera import PICamera
from libraryCH.device.lcd import ILI9341

lcd = ILI9341(LCD_size_w=240, LCD_size_h=320, LCD_Rotate=90)

def wait():
    raw_input('Press Enter')

cap = cv2.VideoCapture(0)

k=np.ones((3,3),np.uint8)

t0 = cap.read()[1]
t1 = cap.read()[1]

while(True):
    

    d=cv2.absdiff(t1,t0)
    
    grey = cv2.cvtColor(d, cv2.COLOR_BGR2GRAY)	

    blur = cv2.GaussianBlur(grey,(5,5),0)	

    ret, th = cv2.threshold( blur, 15, 255, cv2.THRESH_BINARY )

    dilated=cv2.dilate(th,k,iterations=4)	

    contours, hierarchy = cv2.findContours(dilated,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    t2=t0
    cv2.drawContours(t2, contours, -1, (0,255,0), 2 )

    lcd.displayImg(t2)

    t0=t1
    t1=cap.read()[1]    

    if cv2.waitKey(5) == 27 :
        break


cap.release()
