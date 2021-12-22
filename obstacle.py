import cv2
import numpy as np

image = cv2.imread('images/footpath.jpg')
cv2.waitKey(0)

# Grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Find Canny edges
edged = cv2.Canny(gray, 30, 200)
cv2.waitKey(0)

# Finding Contours
contours, hierarchy = cv2.findContours(edged,
	cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

cv2.imshow('Canny Edges After Contouring', edged)
cv2.waitKey(0)

print("Number of Contours found = " + str(len(contours)))

for i, cnt in enumerate(contours):
    if cv2.contourArea(cnt) > 500:
        x,y,w,h = cv2.boundingRect(cnt)

        # draw the biggest contour (c) in green
        cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)

# cv2.drawContours(image, contours, -1, (0, 255, 0), 3)

cv2.imshow('Contours', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
