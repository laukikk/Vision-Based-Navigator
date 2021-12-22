import cv2
import numpy as np

# yolo.py: 

def get_output_layers(net):
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    return output_layers

def draw_prediction(img, class_id, confidence, x, y, x_plus_w, y_plus_h, classes, COLORS):

    label = str(classes[class_id])
    color = COLORS[class_id]
    h = img.shape[1]

    cv2.rectangle(img, (x,y), (x_plus_w,y_plus_h), color, 2)
    cv2.putText(img, label, (x-10,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    cv2.line(img, (x,y_plus_h), (x,h), (255,255,255), 1)

    print('Distance: ' + str(h-y_plus_h) + ' pixels')

def changePerspective(img, draw=0):
    pts = [[345,220],[468,220],[0,420],[750,420]] #Hardcoded values for our usecase
    if draw == 1:
        for point in pts:
            img = cv2.circle(img, point, 5, (0,255,0), -1)

    pts1 = np.float32(pts)
    pts2 = np.float32([[0,0],[150,0],[0,600],[150,600]])
    M = cv2.getPerspectiveTransform(pts1,pts2)
    dst = cv2.warpPerspective(img,M,(150,600))
    return dst

# lane_detection.py: 

def canny_edge_detector(image):
      
    # Convert the image color to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 
      
    # Reduce noise from the image
    blur = cv2.GaussianBlur(gray_image, (5, 5), 0) 
    canny = cv2.Canny(blur, 50, 150)
    return canny

def region_of_interest(image):
    height = image.shape[0]
    polygons = np.array([
        [(200, height), (1100, height), (550, 250)]
        ])
    mask = np.zeros_like(image)
      
    # Fill poly-function deals with multiple polygon
    cv2.fillPoly(mask, polygons, 255) 
      
    # Bitwise operation between canny image and mask image
    masked_image = cv2.bitwise_and(image, mask) 
    return masked_image

def create_coordinates(image, line_parameters):
    slope, intercept = line_parameters
    y1 = image.shape[0]
    y2 = int(y1 * (3 / 5))
    x1 = int((y1 - intercept) / slope)
    x2 = int((y2 - intercept) / slope)
    return np.array([x1, y1, x2, y2])

def create_coordinates(image, line_parameters):
    slope, intercept = line_parameters
    y1 = image.shape[0]
    y2 = int(y1 * (3 / 5))
    x1 = int((y1 - intercept) / slope)
    x2 = int((y2 - intercept) / slope)
    return np.array([x1, y1, x2, y2])

def average_slope_intercept(image, lines):
    left_fit = []
    right_fit = []
    for line in lines:
        x1, y1, x2, y2 = line.reshape(4)
          
        # It will fit the polynomial and the intercept and slope
        parameters = np.polyfit((x1, x2), (y1, y2), 1) 
        slope = parameters[0]
        intercept = parameters[1]
        if slope < 0:
            left_fit.append((slope, intercept))
        else:
            right_fit.append((slope, intercept))
              
    left_fit_average = np.average(left_fit, axis = 0)
    right_fit_average = np.average(right_fit, axis = 0)
    left_line = create_coordinates(image, left_fit_average)
    right_line = create_coordinates(image, right_fit_average)
    return np.array([left_line, right_line])

def display_lines(image, lines):
    line_image = np.zeros_like(image)
    if lines is not None:
        for x1, y1, x2, y2 in lines:
            cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 10)
    return line_image

