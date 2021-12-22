import cv2
import numpy as np
import matplotlib.pyplot as plt
from functions import *

# Path of dataset directory
cap = cv2.VideoCapture("assets/test1.mp4")
while(cap.isOpened()):
	_, frame = cap.read()
	canny_image = canny_edge_detector(frame)
	cropped_image = region_of_interest(canny_image)
	
	lines = cv2.HoughLinesP(cropped_image, 2, np.pi / 180, 100,
							np.array([]), minLineLength = 40,
							maxLineGap = 5)
	
	averaged_lines = average_slope_intercept(frame, lines)
	line_image = display_lines(frame, averaged_lines)
	combo_image = cv2.addWeighted(frame, 0.8, line_image, 1, 1)
	cv2.imshow("results", combo_image)
	
	# When the below two will be true and will press the 'q' on
	# our keyboard, we will break out from the loop
	
	# # wait 0 will wait for infinitely between each frames.
	# 1ms will wait for the specified time only between each frames
	if cv2.waitKey(1) & 0xFF == ord('q'):	
		break

# close the video file
cap.release()

# image = cv2.imread('assets/footpath.jpg')
# canny_image = canny_edge_detector(image)
# cropped_image = region_of_interest(canny_image)

# lines = cv2.HoughLinesP(cropped_image, 2, np.pi / 180, 100,
#                         np.array([]), minLineLength = 40,
#                         maxLineGap = 5)

# averaged_lines = average_slope_intercept(image, lines)
# line_image = display_lines(image, averaged_lines)
# combo_image = cv2.addWeighted(image, 0.8, line_image, 1, 1)
# cv2.imshow("results", combo_image)
# cv2.waitKey(0)

# destroy all the windows that is currently on
cv2.destroyAllWindows()
