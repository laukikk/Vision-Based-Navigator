import cv2
import os
from gtts import gTTS

from functions import *

cap = cv2.VideoCapture("assets/footpath-clip-1.mp4")

sayCommand = 0
commandDelay = 50
  
while(True):
    ret, frame = cap.read()
    # frame = cv2.imread('assets/tiles.jpeg')
    frame = cv2.resize(frame, (1280, 720))
     
    lineImage, image_perspective = changePerspective(frame)
    cv2.imshow('lineImage', lineImage)
    cv2.imshow('image_perspective', image_perspective)

    colour_thresh, image = colourThresholdingHSV(image_perspective)
    cv2.imshow('colour_thresh', centerLines(colour_thresh))
    cv2.imshow('image', centerLines(image))

    x1 = int(image.shape[1]*3/8)
    x2 = int(image.shape[1]*5/8)
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

    print(f'Command : {sayCommand}')

    if not sayCommand:
        if leftContours:
            if rightContours:
                sayCommand = commandDelay
                print('STOP')
                output = gTTS(text = "Stop")
                output.save("output.mp3") 
                os.system("start output.mp3")
            else:
                print('Go Right')
                sayCommand = commandDelay
                output = gTTS(text = "Go Right")
                output.save("output.mp3") 
                os.system("start output.mp3")
        elif rightContours:
            print('Go Left')
            sayCommand = commandDelay
            output = gTTS(text = "Go Left")
            output.save("output.mp3") 
            os.system("start output.mp3")
    else:
        sayCommand -= 1

    if cv2.waitKey(0) & 0xFF == ord('q'):
        break
    
  
cap.release()
cv2.destroyAllWindows()