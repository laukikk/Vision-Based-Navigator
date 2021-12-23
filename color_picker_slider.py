import cv2
import numpy as np
import copy
from functions import *

# optional argument for trackbars
def nothing(x):
    pass

def displayLiveImage(screenImage, imgToAdd, text, boxHeight, boxWidth, topX, topY):
    imgHeight      = imgToAdd.shape[0]
    imgWidth       = imgToAdd.shape[1]
    imgHeightRatio = imgHeight / boxHeight
    imgWidthRatio  = imgWidth / boxWidth
    # findout which side is bigger than box dimension?
    if imgHeightRatio > imgWidthRatio:
        ratio = round(imgHeightRatio+.5,0)
    else:
        ratio = round(imgWidthRatio+.5,0)
    newW = int(imgWidth/ratio)
    newH = int(imgHeight/ratio)
    
    imgToAdd = cv2.resize(imgToAdd, (newW,newH), interpolation = cv2.INTER_CUBIC)
    screenImage[topY:topY+newH, topX:topX+newW] = imgToAdd                               ## ADD image
    #=========IMAGE ADDED ===============================================================================
    topLeftCorner     = topX, topY
    bottomRightCorner =  (topX+boxWidth, topY+boxHeight )
    boxColor = (255,0,0)
    screenImage  = cv2.rectangle(screenImage, topLeftCorner, bottomRightCorner, boxColor, 1)    ## ADD Border to image

    fontColor = (0,0,0)
    screenImage  = cv2.putText(screenImage, text  , (topX+10,topY+int(boxHeight-10)), cv2.FONT_HERSHEY_SIMPLEX, .5, fontColor, 1)


if __name__ == "__main__":
    barsWindow = 'Bars'
    hl = 'H Low'
    hh = 'H High'
    sl = 'S Low'
    sh = 'S High'
    vl = 'V Low'
    vh = 'V High'
    szL = 'Sz Lower'
    szH = 'Sz Higher'

    canvasImage = np.array([[[255, 255, 255]]*1000]*1000, dtype=np.uint8)
    cv2.imwrite('canvasImage.png', canvasImage)

    # create window for the slidebars
    cv2.namedWindow(barsWindow, flags = cv2.WINDOW_GUI_EXPANDED)

    # create the sliders
    cv2.createTrackbar(hl, barsWindow, 0, 179, nothing)
    cv2.createTrackbar(hh, barsWindow, 0, 179, nothing)
    cv2.createTrackbar(sl, barsWindow, 0, 255, nothing)
    cv2.createTrackbar(sh, barsWindow, 0, 255, nothing)
    cv2.createTrackbar(vl, barsWindow, 0, 255, nothing)
    cv2.createTrackbar(vh, barsWindow, 0, 255, nothing)
    cv2.createTrackbar(szL, barsWindow, 0, 1000, nothing)
    cv2.createTrackbar(szH, barsWindow, 0, 1000, nothing)

    # set color default ===============================
    colFilter = (0,179,0,255,0,255)
    lowerBound = 20
    upperBound = 100
    objColor = (0,0,255)

    while True:
        HL = colFilter[0]
        cv2.setTrackbarPos(hl, barsWindow, HL)
        cv2.setTrackbarPos(hh, barsWindow, colFilter[1])
        cv2.setTrackbarPos(sl, barsWindow, colFilter[2])
        cv2.setTrackbarPos(sh, barsWindow, colFilter[3])
        cv2.setTrackbarPos(vl, barsWindow, colFilter[4])
        cv2.setTrackbarPos(vh, barsWindow, colFilter[5])
        cv2.setTrackbarPos(szL, barsWindow, lowerBound)
        cv2.setTrackbarPos(szH, barsWindow, upperBound)

        colorLower = np.array([colFilter[0],colFilter[1],colFilter[2]])    #BGR   112
        colorUpper = np.array([colFilter[3],colFilter[4],colFilter[5]])    # 124


        cap = cv2.VideoCapture("assets/f2_moving camera.mp4")
        while(True):
            ret, frame = cap.read()

            frame = cv2.medianBlur(frame, 9)
            lineImage, frame = changePerspective(frame)
            cv2.imshow('frame', frame)
            cv2.imshow('lineImage', lineImage)

            frame = frame[int(frame.shape[0]/2):, :]
            frame = cv2.pyrUp(frame)
            
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            # read trackbar positions for all
            hul = cv2.getTrackbarPos(hl, barsWindow)
            huh = cv2.getTrackbarPos(hh, barsWindow)
            sal = cv2.getTrackbarPos(sl, barsWindow)
            sah = cv2.getTrackbarPos(sh, barsWindow)
            val = cv2.getTrackbarPos(vl, barsWindow)
            vah = cv2.getTrackbarPos(vh, barsWindow)
            sizeL = (cv2.getTrackbarPos(szL, barsWindow))**2
            sizeH = (cv2.getTrackbarPos(szH, barsWindow))**2

            # make array for final values
            HSVLOW = np.array([hul, sal, val])
            HSVHIGH = np.array([huh, sah, vah])

            # apply the range on a mask
            mask = cv2.inRange(hsv, HSVLOW, HSVHIGH)
            maskedFrame = cv2.bitwise_and(frame, frame, mask = mask)

            # Count the contours on masked frame
            cv2.imwrite("masked.png",maskedFrame)
            masked1 = cv2.imread("masked.png",1)
            kernel = np.ones((5,5),np.uint8)
            masked2 = cv2.dilate(masked1     , kernel, iterations = 1)
            masked           = cv2.cvtColor(masked2,      cv2.COLOR_BGR2GRAY)
            Contours, hierarchy = cv2.findContours(masked, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            marked = copy.copy(frame)
            # print("Contours found", len(Contours),"=========================",sizeL, sizeH)
            rangeCount = 0

            for i in range (0, len(Contours)):
                cnt = Contours[i]
                x,y,w,h = cv2.boundingRect(cnt)
                area = cv2.contourArea(cnt)
                if  sizeL <area  < sizeH:
                    rangeCount = rangeCount + 1
                    cv2.drawContours(marked, [cnt], -1, objColor, 3)

            # display the camera and masked images
            cv2.imshow('Masked', maskedFrame)
            cv2.imshow('Camera', frame)
            cv2.imshow('contours found', marked)

            #build live canvas ===========================
            screenImage = cv2.imread('canvasImage.png',1)
            boxHeight = 210
            boxWidth  = 220
            topX = 30
            topY = 120
            text = "Camera"
            displayLiveImage(screenImage, frame, text, boxHeight, boxWidth, topX, topY)
            
            
            boxHeight = 210
            boxWidth  = 220
            topX = 260
            topY = 120
            text = "ColorDetected"
            displayLiveImage(screenImage, maskedFrame, text, boxHeight, boxWidth, topX, topY)

            boxHeight = 210
            boxWidth  = 220
            topX = 520
            topY = 120
            text = "Dots found"
            displayLiveImage(screenImage, marked, text, boxHeight, boxWidth, topX, topY)

            mesgText = "Dots found: " + str(rangeCount)
            if rangeCount == 3:
                textColor = (0,255,0)
            else:
                textColor = (0,0,255)
            screenImage  = cv2.putText(screenImage, mesgText ,(260,100), cv2.FONT_HERSHEY_SIMPLEX, .6, textColor, 2)
        
            cv2.imshow('RESULT', screenImage)

            if cv2.waitKey(0) & 0xFF == ord('q'):
                break
        
        cap.release()
        # cv2.destroyAllWindows()

