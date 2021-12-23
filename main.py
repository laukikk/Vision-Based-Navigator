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

    colour_thresh, image = colourThresholdingHSV(image_perspective)
    cv2.imshow('colour_thresh', centerLines(colour_thresh))
    cv2.imshow('image', centerLines(image))

    x1 = int(image.shape[1]/4)
    x2 = int(image.shape[1]*3/4)
    mid = int(image.shape[1]/2)
    leftImage = image[:, x1:mid]
    leftThresh = colour_thresh[:, x1:mid]
    rightImage = image[:, mid:x2]
    rightThresh = colour_thresh[:, mid:x2]

    leftMarked, leftContours = getContours(leftImage, leftThresh)
    cv2.imshow('leftMarked', centerLines(leftMarked))
    rightMarked, rightContours = getContours(rightImage, rightThresh)
    cv2.imshow('rightMarked', centerLines(rightMarked))

    marked, contours = getContours(image, colour_thresh)
    cv2.imshow('marked', centerLines(marked))

    if leftContours:
        print(f'Left: {leftContours}')
        if rightContours:
            print(f'Right: {rightContours}')
            print('------ STOP\n')
        else: 
            print('-------- GO RIGHT\n')
    elif rightContours:
        print('-------- GO LEFT\n')

    if cv2.waitKey(0) & 0xFF == ord('q'):
        break
    
  
cap.release()
cv2.destroyAllWindows()