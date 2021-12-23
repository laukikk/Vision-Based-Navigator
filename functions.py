import cv2
import numpy as np
import matplotlib.pyplot as plt

kLeftBottomGap = 50
kLeftTopGap = 600
kTopGap = 200
resolution = [1280, 720]
outputSize = [300, 600]
leftTop = [kLeftTopGap,kTopGap]
rightTop = [resolution[0]-kLeftTopGap,kTopGap]
leftBottom = [kLeftBottomGap,resolution[1]]
rightBottom = [resolution[0]-kLeftBottomGap,resolution[1]]

def changePerspective(img, draw=0):
    # LT, RT, LB, RB
    pts = [leftTop,rightTop,leftBottom,rightBottom]
    # pts = [[345,220],[468,220],[0,420],[750,420]] #Hardcoded values for our usecase
    if draw == 1:
        for point in pts:
            img = cv2.circle(img, point, 5, (0,255,0), -1)

    pts1 = np.float32(pts)
    pts2 = np.float32([[0,0],[outputSize[0],0],[0,outputSize[1]],[outputSize[0],outputSize[1]]])
    M = cv2.getPerspectiveTransform(pts1,pts2)
    dst = cv2.warpPerspective(img,M,outputSize)

    colour = (0, 255, 0)
    thickness = 3
    img = cv2.line(img, leftBottom, leftTop, colour, thickness)
    img = cv2.line(img, rightBottom, rightTop, colour, thickness)

    return img, dst

def convertBinary(image):
    img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.blur(img,(5,5))
    thresh = cv2.threshold(blur,100,255,cv2.THRESH_BINARY)[-1]
    return thresh

def adaptiveThresholding(image, blur):
    if len(image.shape) != 2:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
    img = cv2.medianBlur(gray,blur)

    ret,th1 = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
    th2 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
                cv2.THRESH_BINARY,11,2)
    th3 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
                cv2.THRESH_BINARY,11,2)

    return th2, th3

# def otsuBinarization(image):


def getCoords(event,x,y,flags,img):

    if event == cv2.EVENT_LBUTTONDBLCLK:
        print(x, y)
        cv2.circle(img,(x,y),3,(255,0,0),-1)

if __name__ == '__main__':
    pass