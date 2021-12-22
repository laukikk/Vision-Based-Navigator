import cv2
import numpy as np
import matplotlib.pyplot as plt
from functions import *

cap = cv2.VideoCapture("assets/f2_moving camera.mp4")
  
while(True):
    ret, frame = cap.read()
     
    lineImage, image_perspective = changePerspective(frame)
    cv2.imshow('lineImage', lineImage)
    cv2.imshow('image_perspective', image_perspective)

    image_binary = convertBinary(image_perspective)
    cv2.imshow('image_binary', image_binary)

    mean_thresholding, gaussian_thresholding = adaptiveThresholding(image_perspective, 9)
    cv2.imshow('mean_thresholding_1', mean_thresholding)
    cv2.imshow('gaussian_thresholding_1', gaussian_thresholding)

    mean_thresholding, gaussian_thresholding = adaptiveThresholding(image_perspective, 5)
    cv2.imshow('mean_thresholding_2', mean_thresholding)
    cv2.imshow('gaussian_thresholding_2', gaussian_thresholding)


    if cv2.waitKey(0) & 0xFF == ord('q'):
        break
    
  
cap.release()
cv2.destroyAllWindows()