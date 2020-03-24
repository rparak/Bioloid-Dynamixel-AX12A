#########################################################################################################
# ============================== BRNO UNIVERSITY OF TECHNOLOGY ======================================== #
# ============================== FACULTY OF MECHANICAL ENGINEERING ==================================== #
# =========================INSITUTE OF AUTOMATION AND COMPUTER SCIENCE ================================ #
# Autor: Roman Parak
#########################################################################################################

import cv2
import sys
import numpy as np

from tkinter import *
import time
import threading

class HSV_init_scale:
    def __init__(self):
        self.H_L = 0
        self.S_L = 0
        self.V_L = 0
        self.H_U = 125
        self.S_U = 255
        self.V_U = 255

        self.lower_canny = 0
        self.upper_canny = 0
        # main button
        self.m_b_var   = 0
def init_current_scale(root, hsv_var):
    return Scale(root, from_=0, to=255, length=800, tickinterval=10, orient=HORIZONTAL, command=lambda v: setattr(scale_hsv, hsv_var, v))
def set_var_m_B(var, scale):
    scale.m_b_var   = 1
def main_loop_scale(scale):
    root=Tk()
    root.title('HSV')
    hsv_var = ['H_L','S_L','V_L','H_U','S_U','V_U', 'lower_canny', 'upper_canny']
    
    s   = []
    hsv = [0, 0, 0, 125, 255, 255, 0, 0]
    for i in range(0,len(hsv_var)):
        s = init_current_scale(root, hsv_var[i])
        s.set(hsv[i])
        s.pack()
    
    m_B = Button(root, text ="Confirm color", command=lambda *args: set_var_m_B(1, scale)).pack(anchor=SW)

    root.mainloop()
def object_detection():
    # initialization device {camera}
    device = 1
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
    
    # define global class for scale
    global scale_hsv
    # initialization class for scale
    scale_hsv = HSV_init_scale()
    # threading scale_loop
    threading.Thread(target=main_loop_scale, args=(scale_hsv,)).start()
    
    while True:
        # recording
        _, frame = cam.read()
        
        hsv  = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        blur = cv2.GaussianBlur(hsv, (5, 5), 0)

        # HSV - coordinates of the detected object
        lower_blue = np.array([scale_hsv.H_L, scale_hsv.S_L, scale_hsv.V_L], dtype=np.uint8)
        upper_blue = np.array([scale_hsv.H_U, scale_hsv.S_U, scale_hsv.V_U], dtype=np.uint8)

        kernel_m   = np.ones((5, 5),np.uint8)
        mask       = cv2.inRange(blur, lower_blue, upper_blue)

        open_morph = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel_m)

        result = cv2.bitwise_and(frame, frame, mask = open_morph)

        if scale_hsv.m_b_var == 1:
            # print result HSV {lower, upper}
            print(scale_hsv.H_L, scale_hsv.S_L, scale_hsv.V_L, scale_hsv.H_U, scale_hsv.S_U, scale_hsv.V_U)
            scale_hsv.m_b_var = 0
        
        #cv2.imshow('Window - Edge', np.hstack([edge_auto, edge_w]))
        cv2.imshow('Window - Normal',frame)
        #cv2.imshow('Window - Threshold', mask)
        cv2.imshow('GaussianBlur', blur)
        cv2.imshow('Morphology', open_morph)
        #cv2.imshow('Window - Final Result',result)

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
    
    
