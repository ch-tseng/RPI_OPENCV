#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import cv2

from libraryCH.device.camera import PICamera
from libraryCH.device.lcd import ILI9341

def wait():
    raw_input('Press Enter')

#LCD顯示設定------------------------------------
lcd = ILI9341(LCD_size_w=240, LCD_size_h=320, LCD_Rotate=90)

image=cv2.imread('/home/pi/ebook/Chapter09/images/barcode.png',1)
input = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

hor_der = cv2.Sobel(input, ddepth = -1 , dx = 1, dy = 0, ksize = 5)
ver_der = cv2.Sobel(input, ddepth = -1 , dx = 0, dy = 1, ksize = 5)

diff = cv2.subtract(hor_der, ver_der)
diff = cv2.convertScaleAbs(diff)

lcd.displayImg(diff)
wait()

blur = cv2.GaussianBlur(diff, (3, 3),0)

lcd.displayImg(blur)
wait()

ret, th = cv2.threshold(blur, 225, 255, cv2.THRESH_BINARY)

lcd.displayImg(th)
wait()

dilated = cv2.dilate(th, None, iterations = 10)

lcd.displayImg(dilated)
wait()

eroded = cv2.erode(dilated, None, iterations = 15)

lcd.displayImg(eroded)
wait()

(contours, hierarchy) = cv2.findContours(eroded, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

areas = [cv2.contourArea(temp) for temp in contours]
max_index = np.argmax(areas)
largest_contour=contours[max_index]

x,y,width,height = cv2.boundingRect(largest_contour)
cv2.rectangle(image,(x,y),(x+width,y+height),(0,255,0),8)

lcd.displayImg(image)
wait()
