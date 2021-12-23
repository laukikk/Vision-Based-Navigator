#  1. identify contours of specific colot
#  2. count contours
#  3. Display in real time.   original image, identified  dots, count and resultText 
import cv2 as cv
import numpy as np
import copy

# optional argument for trackbars
def nothing(x):
    pass

def scaleImage(src, scale_percent):
    if scale_percent == 0:
        scale_percent = 50

    #calculate the 50 percent of original dimensions
    width = int(src.shape[1] * scale_percent / 100)
    height = int(src.shape[0] * scale_percent / 100)

    # dsize
    dsize = (width, height)

    # resize image
    output = cv.resize(src, dsize)
    return output

def displayLiveImage(screenImage, imgToAdd,text, boxHeight,boxWidth, topX,topY):
    imgHeight= imgToAdd.shape[0]
    imgWidth= imgToAdd.shape[1]
    imgHeightRatio = imgHeight / boxHeight
    imgWidthRatio  = imgWidth / boxWidth
    # findout which side is bigger than box dimension?
    if imgHeightRatio > imgWidthRatio:
        ratio = round(imgHeightRatio+.5,0)
    else:
        ratio = round(imgWidthRatio+.5,0)
    newW = int(imgWidth/ratio)
    newH = int(imgHeight/ratio)
    
    #print ("box      H W", boxHeight, boxWidth, boxWidth/boxHeight)
    #print ("img      H W", imgHeight, imgWidth)
    #print ("imgRatio H W", imgHeightRatio, imgWidthRatio, ratio)
    #print ("imgNew   H W", newH, newW, newW/newH)
    imgToAdd = cv.resize(imgToAdd, (newW,newH), interpolation = cv.INTER_CUBIC)
    screenImage[topY:topY+newH, topX:topX+newW, ] = imgToAdd                               ## ADD image
    #=========IMAGE ADDED ===============================================================================
    topLeftCorner     = topX, topY
    bottomRightCorner =  (topX+boxWidth, topY+boxHeight )
    boxColor = (255,0,0)
    screenImage  = cv.rectangle(screenImage, topLeftCorner, bottomRightCorner, boxColor, 1)    ## ADD Border to image

    fontColor = (0,0,0)
    screenImage  = cv.putText(screenImage, text  , (topX+10,topY+int(boxHeight-10)), cv.FONT_HERSHEY_SIMPLEX, .5, (0,0,0), 1)




########## MAIN CODE =========================
# named ites for easy reference
barsWindow = 'Bars'
hl = 'H Low'
hh = 'H High'
sl = 'S Low'
sh = 'S High'
vl = 'V Low'
vh = 'V High'
szL = 'Sz Lower'
szH = 'Sz Higher'

# Choose source - stored image of Live  camera feed
source="Image"   #  Options:  Image  / Video

# set up for video capture on camera 0
cap = cv.VideoCapture(0)
#3. CV_CAP_PROP_FRAME_WIDTH Width of the frames in the video stream.
#4. CV_CAP_PROP_FRAME_HEIGHT Height of the frames in the video stream.
#10 CV_CAP_PROP_BRIGHTNESS   #0-255 Brightness of the image (only for cameras).
#11 CV_CAP_PROP_CONTRAST     #0-255 Contrast of the image (only for cameras).
#12 CV_CAP_PROP_SATURATION   #0-255 Saturation of the image (only for cameras).
#13 CV_CAP_PROP_HUE          #13,13 Hue of the image (only for cameras).
#14 CV_CAP_PROP_GAIN         #0-127 Gain of the image (only for cameras).
#15 CV_CAP_PROP_EXPOSURE     #-7 to-1 Exposure (only for cameras)
#17 CV_CAP_PROP_WHITE_BALANCE  4000-7000  white balance     
#cap.set(CV_CAP_PROP_BUFFERSIZE,1)
focdist = 55
brightness = 140
contrast = 38
sat = 144
resolution = "Normal"
if resolution == "High":
    print("SETTING HIGH RESLUTION")
    cap.set(3,1920)
    cap.set(4,1080)
else:
    cap.set(3,1024)
    cap.set(4,768)
cap.set(10,brightness)  #Brightness 0-255
cap.set(11,contrast)   #Contrast 0-255
cap.set(12,sat)   #Saturation 0-255  was 20

#frame = cv.imread("RearAxleRing3.png",1)

frame = cv.imread('assets/footpath.jpg')
frame = cv.pyrDown(frame)
# create window for the slidebars
cv.namedWindow(barsWindow, flags = cv.WINDOW_GUI_EXPANDED)

# create the sliders
cv.createTrackbar(hl, barsWindow, 0, 359, nothing)
cv.createTrackbar(hh, barsWindow, 0, 359, nothing)
cv.createTrackbar(sl, barsWindow, 0, 255, nothing)
cv.createTrackbar(sh, barsWindow, 0, 255, nothing)
cv.createTrackbar(vl, barsWindow, 0, 255, nothing)
cv.createTrackbar(vh, barsWindow, 0, 255, nothing)
cv.createTrackbar(szL, barsWindow, 0, 8000, nothing)
cv.createTrackbar(szH, barsWindow, 0, 4000000, nothing)

# set color default ===============================
colFilter = (0,255,0,255,0,255)
size = "large"
if size == "small":
    lowerBound = 20
    upperBound = 100
elif size == "medium":
    lowerBound = 25
    upperBound = 270
elif size == "large":
    lowerBound = 100
    upperBound = 2500000
while True:
    color = input("select color RED YELLOW GREEN BLUE BLACK")
    
    if color == "":
        color = "BLACK"
    print("Color Selected is ", color)
    if color == "RED":
        colFilter = (1,14,0,255,0,255)
        objColor = (0,0,255)
    elif color == "YELLOW":
        #working version========
        #colorLower = np.array([0, 120, 120])    #GBR  ==========   112
        #colorUpper = np.array([124, 255, 255])    # 124
        colFilter = (11,26,6,255,3,255)
        objColor = (0,255,255) 
    elif color == "GREEN":
        colFilter = (59,77,83,242,0,255)
        #colorLower = np.array([0,0,0])
        #colorUpper = np.array([350,55,100])
        objColor = (37,33,251)
    elif color == "BLUE":
        colFilter = (110,127,83,242,0,255)
        #colorLower = np.array([0,0,0])
        #colorUpper = np.array([350,55,100])
        objColor = (37,33,251)
    elif color == "WHITE":
        colFilter = (0,350,0,55,0,100)
        #colorLower = np.array([0,0,0])
        #colorUpper = np.array([350,55,100])
        objColor = (255,255,255)
    elif color == "BLACK":
        colFilter = (0,0,0,55,0,100)
        #colorLower = np.array([0,0,0])
        #colorUpper = np.array([350,55,100])
        objColor = (255,255,255)
    
    HL = colFilter[0]
    cv.setTrackbarPos(hl, barsWindow, HL)
    cv.setTrackbarPos(hh, barsWindow, colFilter[1])
    cv.setTrackbarPos(sl, barsWindow, colFilter[2])
    cv.setTrackbarPos(sh, barsWindow, colFilter[3])
    cv.setTrackbarPos(vl, barsWindow, colFilter[4])
    cv.setTrackbarPos(vh, barsWindow, colFilter[5])
    cv.setTrackbarPos(szL, barsWindow, lowerBound)
    cv.setTrackbarPos(szH, barsWindow, upperBound)

    colorLower = np.array([colFilter[0],colFilter[1],colFilter[2]])    #BGR   112
    colorUpper = np.array([colFilter[3],colFilter[4],colFilter[5]])    # 124



    while(True):
        if source == "Video":
            ret, frame = cap.read()
            if not ret:
                print("Issue in capturing Frame")
                #cap = cv.VideoCapture(0)
                #continue
        else:
            
            pass

        #frame = cv.GaussianBlur(frame, (5, 5), 0)
        # convert to HSV from BGR
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

        # read trackbar positions for all
        hul = cv.getTrackbarPos(hl, barsWindow)
        huh = cv.getTrackbarPos(hh, barsWindow)
        sal = cv.getTrackbarPos(sl, barsWindow)
        sah = cv.getTrackbarPos(sh, barsWindow)
        val = cv.getTrackbarPos(vl, barsWindow)
        vah = cv.getTrackbarPos(vh, barsWindow)
        sizeL = (cv.getTrackbarPos(szL, barsWindow))**2
        sizeH = (cv.getTrackbarPos(szH, barsWindow))**2

        # make array for final values
        HSVLOW = np.array([hul, sal, val])
        HSVHIGH = np.array([huh, sah, vah])

        # apply the range on a mask
        mask = cv.inRange(hsv, HSVLOW, HSVHIGH)
        maskedFrame = cv.bitwise_and(frame, frame, mask = mask)

        # Count the contours on masked frame
        cv.imwrite("masked.png",maskedFrame)
        masked1 = cv.imread("masked.png",1)
        kernel = np.ones((5,5),np.uint8)
        masked2 = cv.dilate(masked1     , kernel, iterations = 1)
        masked           = cv.cvtColor(masked2,      cv.COLOR_BGR2GRAY)
        Contours, hierarchy = cv.findContours(masked, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        marked = copy.copy(frame)
        print("Contours found", len(Contours),"=========================",sizeL, sizeH)
        rangeCount = 0
        for i in range (0, len(Contours)):
            cnt = Contours[i]
            x,y,w,h = cv.boundingRect(cnt)
            area = cv.contourArea(cnt)
            if  sizeL <area  < sizeH:
                rangeCount = rangeCount + 1
                #print("\t\tContour ",i, "\t\tcountourArea", cv.contourArea(cnt),"matched ++++++++") 
                cv.drawContours(marked, [cnt], -1, objColor, 3)
                #marked  = cv.putText(marked, str(rangeCount) , (x+10,y), cv.FONT_HERSHEY_SIMPLEX, 2.6, (255,255,0), 2)
                maskedFrame  = cv.putText(maskedFrame, str(rangeCount) , (x+10,y), cv.FONT_HERSHEY_SIMPLEX, 2.6, (255,255,0), 2)
                
            else:
                #print("\t\tContour SKIPPED",i, "\t\tcountourArea", cv.contourArea(cnt),".")
                pass
                
        #cv.drawContours(marked, contours, -1, yellow, 3)

        #boxColor = (255,255,255)
        #topLeftCorner = (0,0)
        #bottomRightCorner = (400,100)
        #marked  = cv.rectangle(marked, topLeftCorner, bottomRightCorner, boxColor, -1)    ## ADD Border to image

        
        # display the camera and masked images
        cv.imshow('Masked', maskedFrame)
        cv.imshow('Camera', frame)
        cv.imshow('contours found', marked)

        #build live canvas ===========================
        screenImage= cv.imread("blank-LiveCanvas.jpg",1)
        boxHeight = 210
        boxWidth  = 220
        topX = 30
        topY = 120
        text = "Camera"
        displayLiveImage(screenImage, frame,text, boxHeight,boxWidth, topX,topY)
        
        
        boxHeight = 210
        boxWidth  = 220
        topX = 260
        topY = 120
        text = "ColorDetected"
        displayLiveImage(screenImage, maskedFrame,text, boxHeight,boxWidth, topX,topY)

        boxHeight = 210
        boxWidth  = 220
        topX = 520
        topY = 120
        text = "Dots found"
        displayLiveImage(screenImage, marked,text, boxHeight,boxWidth, topX,topY)

        mesgText = str(color)+" dots found: "+ str(rangeCount)
        if rangeCount == 3:
            textColor = (0,255,0)
        else:
            textColor = (0,0,255)
        screenImage  = cv.putText(screenImage, mesgText , (260,100), cv.FONT_HERSHEY_SIMPLEX, .6, textColor, 2)
      
        cv.imshow('RESULT', screenImage)
        # check for q to quit program with 5ms delay
        if cv.waitKey(5) & 0xFF == ord('q'):
            break

        cap.set(28,focdist)
        cap.set(10,brightness)
        cap.set(11,contrast)
        cap.set(11,sat)
    
        ##################      
        k = cv.waitKey(1)

        if k%256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            break
        elif k%256 == 32:
            # SPACE pressed
            img_name = "29Aug-color-{}.png".format(img_counter)
            #cv2.SetCaptureProperty(imagename,CV_CAP_PROP_BRIGHTNESS,10);
            
            cv.imwrite(img_name, frame)
            print("{} written!".format(img_name))
            img_counter += 1
        elif k%256 == 98: # key B
            print("B")
            focdist = focdist + 5
            cap.set(28,focdist)
        elif k%256 == 99: # key C
            print("C")
            focdist = focdist - 5
            cap.set(28,focdist)
        elif k%256 == 100: # key D
            brightness = brightness + 5
            print("B",brightness)
            cap.set(10,brightness)
        elif k%256 == 101: # key E
            brightness = brightness - 5
            print("B",brightness)
            cap.set(10,brightness)
        elif k%256 == 102: # key F
            contrast = contrast + 2
            cap.set(11,contrast)
        elif k%256 == 103: # key G
            contrast = contrast - 2
            cap.set(11,contrast)
        elif k%256 == 104: # key h
            sat = sat + 2
            cap.set(12,sat)
        elif k%256 == 106: # key J
            sat = sat - 2
            cap.set(11,sat)

# clean up our resources
cap.release()
cv.destroyAllWindows()
