import cv2

def getCoords(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        print(x, y)
        cv2.circle(img,(x,y),3,(255,255,255),-1)

if __name__ == "__main__":
    cap = cv2.VideoCapture("assets/footpath-clip-2.mp4")
    img = None

    while(True):
        ret, frame = cap.read()

        cv2.imshow('frame', frame)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            img = frame
            break
        
    
    cv2.namedWindow('image')
    cv2.setMouseCallback('image',getCoords)

    while(1):
        cv2.imshow('image',img)
        if cv2.waitKey(20) & 0xFF == 27:
            break
    cv2.destroyAllWindows()