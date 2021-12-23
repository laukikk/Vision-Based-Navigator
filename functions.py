import cv2
import numpy as np
import matplotlib.pyplot as plt

kLeftBottomGap = 100
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

def colourThresholdingHSV(image):
    image = image[image.shape[0] - int(image.shape[0]/10):, :]
    image = cv2.pyrUp(image)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    huL = 0
    huH = 179
    saL = 35
    saH = 255
    vaL = 0
    vaH = 255
    HSVLOW = np.array([huL, saL, vaL])
    HSVHIGH = np.array([huH, saH, vaH])

    # apply the range on a mask
    mask = cv2.inRange(hsv, HSVLOW, HSVHIGH)
    maskedFrame = cv2.bitwise_and(image, image, mask = mask)
    
    return maskedFrame, image

def getContours(image, maskedFrame):
    sizeL = 20**2
    sizeH = 450**2
    objColor = (0,0,255)
    marked = image.copy()
    
    # Count the contours on masked frame
    cv2.imwrite("masked.png", maskedFrame)
    masked1 = cv2.imread("masked.png",1)
    kernel = np.ones((5,5),np.uint8)
    masked2 = cv2.dilate(masked1     , kernel, iterations = 1)
    masked  = cv2.cvtColor(masked2,      cv2.COLOR_BGR2GRAY)
    Contours, hierarchy = cv2.findContours(masked, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    rangeCount = 0

    for i in range (0, len(Contours)):
        cnt = Contours[i]
        x,y,w,h = cv2.boundingRect(cnt)
        area = cv2.contourArea(cnt)
        if sizeL < area < sizeH:
            rangeCount = rangeCount + 1
            cv2.drawContours(marked, [cnt], -1, objColor, 3)
            marked = cv2.rectangle(marked, (x, y), (x+w, y+h), (255,255,255), 2)

    return marked, rangeCount

def getCoords(event,x,y,flags,img):

    if event == cv2.EVENT_LBUTTONDBLCLK:
        print(x, y)
        cv2.circle(img,(x,y),3,(255,0,0),-1)

def centerLines(image):
    image = cv2.rectangle(image, (0, int(image.shape[0]/2)), (image.shape[1], int(image.shape[0]/2)), (0,0,0), 2)
    image = cv2.rectangle(image, (int(image.shape[1]/2), 0), (int(image.shape[1]/2), image.shape[0]), (0,0,0), 2)
    return image



if __name__ == '__main__':
    pass