#########################################################################################################
# ============================== BRNO UNIVERSITY OF TECHNOLOGY ======================================== #
# ============================== FACULTY OF MECHANICAL ENGINEERING ==================================== #
# =========================INSITUTE OF AUTOMATION AND COMPUTER SCIENCE ================================ #
# Autor: Roman Parak
#########################################################################################################

import cv2
import sys
import time

def fps_calculation(cam, num_of_frames):
    # print number of frames to capture
    print('Number of capturing frames: ', num_of_frames)
    # start recording time
    start_recording = time.time()

    # grab the initial number of frames
    for i in range(0, num_of_frames) :
        _, frame = cam.read()

    # finish recording
    end_recording = time.time()

    # calculation time of recording
    num_of_sec = end_recording - start_recording

    t_r = str(int(num_of_sec)) + ' s' 
    print('Time of recordning:', t_r)
 
    # calculation frames per second
    fps_result  = num_of_frames / num_of_sec

    # calculation and print result
    fps_r = str(int(fps_result)) + ' fps'
    print('Frames per seconds:', fps_r)

def main(argv=sys.argv):
    # open video
    cam = cv2.VideoCapture(1);

    if not(cam.isOpened()):
        cam.open(1)

    # set frame parameters
    cam.set(3, 640)
    cam.set(4, 480)

    # fps calculation
    fps_calculation(cam, 1000)

    # release window
    cam.release()
if __name__ == '__main__' :
    sys.exit(main())
