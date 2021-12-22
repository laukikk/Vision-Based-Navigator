import cv2
import numpy as np
import matplotlib.pyplot as plt
# from functions import *

def getThreshold(image):
    img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    ret,thresh1 = cv2.threshold(img,100,255,cv2.THRESH_BINARY)
    ret,thresh2 = cv2.threshold(img,127,255,cv2.THRESH_BINARY_INV)
    ret,thresh3 = cv2.threshold(img,127,255,cv2.THRESH_TRUNC)
    ret,thresh4 = cv2.threshold(img,127,255,cv2.THRESH_TOZERO)
    ret,thresh5 = cv2.threshold(img,127,255,cv2.THRESH_TOZERO_INV)

    titles = ['Original Image','BINARY','BINARY_INV','TRUNC','TOZERO','TOZERO_INV']
    images = [image, thresh1, thresh2, thresh3, thresh4, thresh5]

    for i in range(6):
        plt.subplot(2,3,i+1),plt.imshow(images[i],'gray')
        plt.title(titles[i])
        plt.xticks([]),plt.yticks([])

    plt.show()

def pathObstacleContours(image):
    img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.blur(img,(5,5))
    thresh = cv2.threshold(blur,100,255,cv2.THRESH_BINARY)[-1]
    contours,hierarchy = cv2.findContours(thresh,2,1)
    cnt = contours[0]

    hull = cv2.convexHull(cnt,returnPoints = False)
    defects = cv2.convexityDefects(cnt,hull)

    for i in range(defects.shape[0]):
        print('1')
        s,e,f,d = defects[i,0]
        start = tuple(cnt[s][0])
        end = tuple(cnt[e][0])
        far = tuple(cnt[f][0])
        cv2.line(img,start,end,[0,255,0],2)
        cv2.circle(img,far,5,[0,0,255],-1)

    cv2.imshow('img',img)
    cv2.imshow('thresh',thresh)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
def getCoords(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        print(x, y)
        cv2.circle(img,(x,y),3,(255,255,255),-1)


if __name__ == "__main__":
    img = cv2.imread('assets/footpath.jpg', 0)