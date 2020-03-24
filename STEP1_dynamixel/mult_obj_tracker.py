#########################################################################################################
# ============================== BRNO UNIVERSITY OF TECHNOLOGY ======================================== #
# ============================== FACULTY OF MECHANICAL ENGINEERING ==================================== #
# =========================INSITUTE OF AUTOMATION AND COMPUTER SCIENCE ================================ #
# Autor: Roman Parak
#########################################################################################################

import cv2
import sys
import numpy as np
import math
import matplotlib.pyplot as plt
import time

import communication
import dyn_ax_12p
import parameters

import object_draw_bioloid

def present_position(p_d, dC_AX_12p, dyn_id):
  # initialization packet
  packet_command = [p_d.AX_12p_PRESENT_POSITION_L, p_d.AX_12p_RETURN_READ] # AREA {RAM} | STATUS RETURNS LEVELS

  dC_AX_12p.init_packet_param_AX_12p(packet_command)

  if dC_AX_12p.err == None:
    # read
    dC_AX_12p.command_to_AX_12p(p_d.AX_12p_READ_DATA) # INSTRUCTION SET

    # print result
    #print('Present Position: ')

    a = dC_AX_12p.result

    # release of variables
    dC_AX_12p.release_packet_param_AX_12p()
  else:
    print('Error!')

  return a

def present_temperature(p_d, dC_AX_12p, dyn_id):
  # initialization packet
  packet_command = [p_d.AX_12p_PRESENT_TEMPERATURE, p_d.AX_12p_RETURN_READ] # AREA {RAM} | STATUS RETURNS LEVELS

  dC_AX_12p.init_packet_param_AX_12p(packet_command)

  if dC_AX_12p.err == None:
    # read
    dC_AX_12p.command_to_AX_12p(p_d.AX_12p_READ_DATA) # INSTRUCTION SET

    # print result
    print('Present temperature: ' + dC_AX_12p.result)
    # release of variables
    dC_AX_12p.release_packet_param_AX_12p()
  else:
    print('Error!')

  if result_pos != 'None':
    return int(float(dC_AX_12p.result))
  else:
    return 0

def set_speed(p_d, dC_AX_12p, dyn_id, goal_speed):
  # initialization packet
  packet_command = [p_d.AX_12p_GOAL_SPEED_L, goal_speed] # AREA {RAM} 

  dC_AX_12p.init_packet_param_AX_12p(packet_command)

  if dC_AX_12p.err == None:
    # write
    dC_AX_12p.command_to_AX_12p(p_d.AX_12p_WRITE_DATA) # INSTRUCTION SET

    # release of variables
    dC_AX_12p.release_packet_param_AX_12p()
  else:
    print('Error!')
def set_position(p_d, dC_AX_12p, dyn_id, goal_pos):
  # initialization packet
  packet_command = [p_d.AX_12p_GOAL_POSITION_L, goal_pos] # AREA {RAM}

  dC_AX_12p.init_packet_param_AX_12p(packet_command)

  if dC_AX_12p.err == None:
    # write
    dC_AX_12p.command_to_AX_12p(p_d.AX_12p_WRITE_DATA) # INSTRUCTION SET

    # release of variables
    dC_AX_12p.release_packet_param_AX_12p()
  else:
    print('Error!')
def is_motor_moving(p_d, dC_AX_12p, dyn_id):
  # initialization packet
  packet_command = [p_d.AX_12p_MOVING, p_d.AX_12p_RETURN_READ] # AREA {RAM} | STATUS RETURNS LEVELS

  dC_AX_12p.init_packet_param_AX_12p(packet_command)

  if dC_AX_12p.err == None:
    # read
    dC_AX_12p.command_to_AX_12p(p_d.AX_12p_READ_DATA) # INSTRUCTION SET

    # print result
    result = dC_AX_12p.result
    # release of variables
    dC_AX_12p.release_packet_param_AX_12p()
  else:
    print('Error!')

  return int(result)
def mult_obj_tracker(device, frame_width, frame_height):
	# parameters for drawing {plot}
	COUNT_OF_OBJECTS = 2 # each color
	# identical to the frame size
	MIN_X = 0
	MAX_X = 640
	MIN_Y = 480
	MAX_Y = 0

	# number of individual colors for input -> ['blue', 'green']
	b_tObj = object_draw_bioloid.tracking_bioloid(1,1)
	# set maximum limits {x, y} of frame
	b_tObj.axis_init(640, 480)
	# initialization triangles

	# HSV - coordinates of the detected object
	lower_hsv = {
        'green':(17, 71, 78),
        'blue': (97, 63, 34)
	} 

	upper_hsv = {
        'green':(27, 255, 255),
        'blue':(164, 223, 184)
	}
	# initialization colors for ectangle around the object
	colors_cr = {
		'green':(0,255,0),
		'blue':(255,0, 0)
	}

	# start recording
	mult_t = cv2.VideoCapture(device)

	if not(mult_t.isOpened()):
		mult_t.open(device)

	# dynamixel control
	port_name = 'COM4'
	p_d = parameters.param_dyn(port_name)

	# serial port communication
	s_p = communication.Serial_Port(p_d.PORT_NAME, p_d.BAUDRATE)

	dynamixel_id = [1]
	dC_AX_12p    = []

	for init_d in range(0, len(dynamixel_id)):
	  # initial AX-12+
	  aux_dyn = dyn_ax_12p.dynamixel_AX12P(dynamixel_id[init_d], s_p.serial_port)
	  dC_AX_12p.append(aux_dyn)

	# set frame parameters
	mult_t.set(frame_width, 640)
	mult_t.set(frame_height, 480)

	# initialization approx. param
	green_approx_x    = 0
	green_approx_y    = 0
	blue_approx_x   = 0
	blue_approx_y   = 0
	while True:
		_, frame_mT = mult_t.read()

		# convert to grayscale
		hsv  = cv2.cvtColor(frame_mT, cv2.COLOR_BGR2HSV)
		# Gaussian Blur {filter}
		blur = cv2.GaussianBlur(hsv, (5, 5), 0)

		# ============================== detection object ==============================
		for color_k, _ in upper_hsv.items():
			# initialization matrix {kernel}
			kernel_m   = np.ones((5, 5),np.uint8)
			# comparison
			mask_m     = cv2.inRange(blur, lower_hsv[color_k], upper_hsv[color_k])
			# open structure {kernel matrix} -> MORPH_OPEN
			open_morph = cv2.morphologyEx(mask_m, cv2.MORPH_OPEN, kernel_m)
			# find contours
			res_cnts   = cv2.findContours(open_morph.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
			obj_center = None

			for obj_num, obj_contour in enumerate(res_cnts):
				# calculation object perimeter {2*pi*r} - Circle, {2(L + W)} - rectangle
				obj_perimeter = cv2.arcLength(obj_contour, True)
				approx        = cv2.approxPolyDP(obj_contour, 0.02 * obj_perimeter, True)

				if 4 <= len(approx) <= 15:
					#print(len(approx))
					# calculation area of the object {pi*r^2} => circle, {LxW} - rectangle
					obj_area = cv2.contourArea(obj_contour)
					# calculation circularity: formula {4 * pi * Area/(perimeter^2)}
					obj_circ = ((4 * math.pi * obj_area)/(obj_perimeter * obj_perimeter))
		
					# condition of size {area} -> object
					if (50  < obj_area < 1000) and (0.3 < obj_circ < 1.5) and (obj_num == 0):
						# detect coordinates of the object contour {circle}
						(x_c, y_c), obj_radius = cv2.minEnclosingCircle(obj_contour)
						obj_center             = (int(x_c), int(y_c))
						obj_radius             = int(obj_radius)
						#print(obj_area)
						# detect coordinates of the object contour {rectangle}
						x_r, y_r, obj_w, obj_h = cv2.boundingRect(obj_contour)
						# draw rectangle and circle
						obj_rect        	 = cv2.rectangle(frame_mT, (x_r, y_r), (x_r + obj_w, y_r + obj_h), colors_cr[color_k], 2)
						cv2.circle(obj_rect, obj_center, int(obj_radius), colors_cr[color_k], 2)
						# initialization string for the object {text}
						str_aux_x = 'Dx:' + str(int(x_r))
						str_aux_y = 'Dy:' + str(int(480 - y_r))
						# adding text {coordinates}
						cv2.putText(obj_rect, str_aux_x, (int(x_r - 0.5), int(y_r - 20)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, colors_cr[color_k], 2)
						cv2.putText(obj_rect, str_aux_y, (int(x_r - 0.5), int(y_r - 5)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, colors_cr[color_k], 2)

						if color_k == 'green':
							if abs(green_approx_x - int(x_r)) <= 1 or abs(green_approx_y - int(x_r)) <= 1: 
								b_tObj.control_rect(480 - green_approx_y, 480 - blue_approx_y)     
								#b_tObj.plot_block_show()
							else:
								green_approx_x = int(x_r)
								green_approx_y = int(y_r)

						elif color_k == 'blue':
							if abs(blue_approx_x - int(x_r)) <= 1 or abs(blue_approx_y - int(x_r)) <= 1: 
								b_tObj.control_rect(480 - green_approx_y, 480 - blue_approx_y)     
								#b_tObj.plot_block_show()
							else:
								blue_approx_x = int(x_r)
								blue_approx_y = int(y_r)

						set_speed(p_d, dC_AX_12p[0], dynamixel_id[0], 480 - blue_approx_y)
						set_position(p_d, dC_AX_12p[0], dynamixel_id[0], 480 - green_approx_y)

		# show the result in the main frame
		cv2.imshow("Dynamixel AX-12A - OpenCV control", frame_mT)

		# ending condition
		if cv2.waitKey(1) & 0xFF == ord('q'):
			return mult_t
			break

def main(argv=sys.argv):
	# parameters {camera}
	CAM_DEVICE = 0

	CV_CAP_PROP_FRAME_WIDTH  = 3
	CV_CAP_PROP_FRAME_HEIGHT = 4

	# call function {multiple object tracking}
	m_t = mult_obj_tracker(CAM_DEVICE, CV_CAP_PROP_FRAME_WIDTH, CV_CAP_PROP_FRAME_HEIGHT)

	# release and destroy any open windows
	m_t.release()
	cv2.destroyAllWindows()

if __name__ == "__main__":
	sys.exit(main())
