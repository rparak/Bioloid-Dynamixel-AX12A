#########################################################################################################
# ============================== BRNO UNIVERSITY OF TECHNOLOGY ======================================== #
# ============================== FACULTY OF MECHANICAL ENGINEERING ==================================== #
# =========================INSITUTE OF AUTOMATION AND COMPUTER SCIENCE ================================ #
# Autor: Roman Parak
#########################################################################################################

import cv2
import sys
import numpy as np

def object_detection():
    # initialization device {camera}
    device = 0
    # open video
    cam = cv2.VideoCapture(device)
    
    if not(cam.isOpened()):
        cam.open(device)

    CV_CAP_PROP_FRAME_WIDTH  = 3
    CV_CAP_PROP_FRAME_HEIGHT = 4
    
    # set parameters
    cam.set(CV_CAP_PROP_FRAME_WIDTH, 640)
    cam.set(CV_CAP_PROP_FRAME_HEIGHT, 480)
    
    # initialization window {normal, gray}
    cv2.namedWindow('Window - Normal', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Window - Normal', 640, 480)
    
 
    cv2.namedWindow('Window - Threshold', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Window - Threshold', 640, 480)
    # HSV - coordinates of the detected object
    lower_hsv = {
        'red':(171, 75, 126), 
        'green':(40, 58, 84),
        'blue':(79, 55, 93),
        'pink':(100, 56, 129),
        'purple':(114, 15, 48),
        'orange':(10, 88, 144)
    } 

    upper_hsv = {
        'red':(179, 255, 255),
        'green':(93, 255, 255),
        'blue':(150, 255, 255),
        'pink':(169, 191, 209),
        'purple':(249, 71, 245),
        'orange':(20, 255, 229)
    }


    while True:
        # recording
        _, frame = cam.read()
        
        hsv  = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        blur = cv2.GaussianBlur(hsv, (5, 5), 0)

        kernel_m   = np.ones((5, 5),np.uint8)

        mask_red       = cv2.inRange(blur, lower_hsv['red'], upper_hsv['red'])
        open_morph_red = cv2.morphologyEx(mask_red, cv2.MORPH_OPEN, kernel_m)

        mask_green       = cv2.inRange(blur, lower_hsv['green'], upper_hsv['green'])
        open_morph_green = cv2.morphologyEx(mask_green, cv2.MORPH_OPEN, kernel_m)

        mask_blue       = cv2.inRange(blur, lower_hsv['blue'], upper_hsv['blue'])
        open_morph_blue = cv2.morphologyEx(mask_blue, cv2.MORPH_OPEN, kernel_m)

        mask_pink       = cv2.inRange(blur, lower_hsv['pink'], upper_hsv['pink'])
        open_morph_pink = cv2.morphologyEx(mask_pink, cv2.MORPH_OPEN, kernel_m)

        mask_purple       = cv2.inRange(blur, lower_hsv['purple'], upper_hsv['purple'])
        open_morph_purple = cv2.morphologyEx(mask_purple, cv2.MORPH_OPEN, kernel_m)

        mask_orange       = cv2.inRange(blur, lower_hsv['orange'], upper_hsv['orange'])
        open_morph_orange = cv2.morphologyEx(mask_orange, cv2.MORPH_OPEN, kernel_m)


        #mask_b_morph = mask_red + mask_green + mask_blue + mask_pink + mask_purple + mask_orange
        #result_mask   = open_morph_red + open_morph_green + open_morph_blue + open_morph_pink + open_morph_purple + open_morph_orange

        mask_b_morph  = mask_purple
        result_mask   = open_morph_purple

        result = cv2.bitwise_and(frame, frame, mask = result_mask)

        
        #cv2.imshow('Window - Edge', np.hstack([edge_auto, edge_w]))
        cv2.imshow('Window - Normal',frame)
        cv2.imshow('Window - Threshold', mask_b_morph)
        cv2.imshow('GaussianBlur', blur)
        cv2.imshow('Morphology', result_mask)
        cv2.imshow('Window - Final Result',result)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    # release and destroy windows
    cam.release()
    cv2.destroyAllWindows()
def main(argv=sys.argv):
    # call function for video recording {object detection}
    object_detection()
    
if __name__ == "__main__":
    sys.exit(main())
    
    
