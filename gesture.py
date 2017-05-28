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

while(True):

    ret, frame = cap.read()
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    blur=cv2.GaussianBlur(gray,(3,3),0)

    lcd.displayImg(blur)
'''
    ret , th = cv2.threshold(
        blur,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

    lcd.displayImg(th)
'''
