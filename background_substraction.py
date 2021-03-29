# Python code for Background subtraction using OpenCV 
import numpy as np 
import time
import cv2 
  
cap = cv2.VideoCapture('video/mitch2.mp4') 
fgbg = cv2.createBackgroundSubtractorMOG2() 
  
while(1): 
    ret, frame = cap.read() 
  
    fgmask = fgbg.apply(frame) 
   
    time.sleep(1/20)
    cv2.imshow('fgmask', fgmask) 
    cv2.imshow('frame',frame ) 
  
      
    k = cv2.waitKey(30) & 0xff
    if k == 27: 
        break
      
  
cap.release() 
cv2.destroyAllWindows() 