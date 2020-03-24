'''
Created on Jan 15, 2017

@author: roman_parak
'''

import cv2
import sys
import numpy as np
import math
import object_draw_bioloid
import time

import communication
import dyn_ax_12p
import parameters

def set_position(p_d, dC_AX_12p, dyn_id, goal_pos):
	# initialization packet
	packet_command = [p_d.AX_12p_GOAL_POSITION_L, goal_pos]

	dC_AX_12p.init_packet_param_AX_12p(packet_command)

	if dC_AX_12p.err == None:
		dC_AX_12p.command_to_AX_12p(p_d.AX_12p_WRITE_DATA) # INSTRUCTION SET

		# release of variables
		dC_AX_12p.release_packet_param_AX_12p()
	else:
		print('Error!')
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
	# dynamixel parameters for communication {initialization}
	port_name = 'COM4'
	p_d = parameters.param_dyn(port_name)

	# serial port communication
	s_p = communication.Serial_Port(p_d.PORT_NAME, p_d.BAUDRATE)

	# controll dynamixel AX-12+
	dC_AX_12p    = []
	dynamixel_id = [3, 4]

	for init_d in range(0, len(dynamixel_id)):
		# initial AX-12+
		aux_dyn = dyn_ax_12p.dynamixel_AX12P(dynamixel_id[init_d], s_p.serial_port)
		dC_AX_12p.append(aux_dyn)

	# call functions {write speed} 
	goal_speed = 300
	for i_speed in range(0, len(dC_AX_12p)):
		set_speed(p_d, dC_AX_12p[i_speed], dynamixel_id[i_speed], goal_speed)

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
	b_tObj.init_triangles()

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
	
	# initialization colors for circle and rectangle around the object
	colors_cr = {
		'green':(0,255,0),
		'blue':(255,0,0)
	}

	# start recording
	mult_t = cv2.VideoCapture(device)

	if not(mult_t.isOpened()):
		mult_t.open(device)

	# set frame parameters
	mult_t.set(frame_width, 640)
	mult_t.set(frame_height, 480)

	while True:
		_, frame_mT = mult_t.read()

		hsv  = cv2.cvtColor(frame_mT, cv2.COLOR_BGR2HSV)

		blur = cv2.GaussianBlur(hsv, (5,5), 0)

		# ============================== detection object ==============================
		for color_k, _ in upper_hsv.items():
			# initialization matrix {kernel}
			kernel_m   = np.ones((7,7),np.uint8)
			# comparison
			mask_m     = cv2.inRange(blur, lower_hsv[color_k], upper_hsv[color_k])
			# open structure {kernel matrix} -> MORPH_OPEN
			open_morph = cv2.morphologyEx(mask_m, cv2.MORPH_OPEN, kernel_m)
			# find contours
			res_cnts   = cv2.findContours(open_morph.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
			obj_center = None

			for obj_num, obj_contour in enumerate(res_cnts):
				# calculation object perimeter
				obj_perimeter = cv2.arcLength(obj_contour, True)
				approx        = cv2.approxPolyDP(obj_contour, 0.02 * obj_perimeter, True)
				if 6 < len(approx) < 15:
					# calculation area of the object
					obj_area = cv2.contourArea(obj_contour)
					# calculation circularity: formula {4 * pi * Area/(perimeter^2)}
					obj_circ = ((4 * math.pi * obj_area)/(obj_perimeter * obj_perimeter))
	
				    # condition of size {area} -> object
					if (5 < obj_area < 1000) and (0.3 < obj_circ < 1.5): 
						# detect coordinates of the object contour {circle}
						(x_c, y_c), obj_radius = cv2.minEnclosingCircle(obj_contour)
						obj_center             = (int(x_c), int(y_c))
						obj_radius             = int(obj_radius)
						# detect coordinates of the object contour {rectangle}
						x_r, y_r, obj_w, obj_h = cv2.boundingRect(obj_contour)
						# draw rectangle and circle
						obj_rect        	 = cv2.rectangle(frame_mT, (x_r, y_r), (x_r + obj_w, y_r + obj_h), colors_cr[color_k], 2)
						cv2.circle(obj_rect, obj_center, int(obj_radius), colors_cr[color_k], 2)
						# initialization string for the object {text}
						str_aux_x = 'Dx:' + str(int(x_c))
						str_aux_y = 'Dy:' + str(int(y_c))
						# adding text {coordinates}
						cv2.putText(obj_rect, str_aux_x, (int(x_r - 0.5), int(y_r - 20)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, colors_cr[color_k], 2)
						cv2.putText(obj_rect, str_aux_y, (int(x_r - 0.5), int(y_r - 5)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, colors_cr[color_k], 2)
	

						if color_k == 'blue' and int(x_c) > 340:
							b_tObj.loop_draw_object(int(x_c), int(y_c), color_k, 0)
						elif color_k == 'green' and int(x_c) < 260:
							b_tObj.loop_draw_object(int(x_c), int(y_c), color_k, 0)

						# calculation angle
						b_tObj.calculation_of_robot_output()

						# set position {right hand}
						is_mM_dx_Id3 = is_motor_moving(p_d, dC_AX_12p[0], dynamixel_id[0])

						if is_mM_dx_Id3 == 0:
							set_position(p_d, dC_AX_12p[0], dynamixel_id[0], b_tObj.pos_rh)

						# set position {left hand}
						is_mM_dx_Id4 = is_motor_moving(p_d, dC_AX_12p[1], dynamixel_id[1])

						if is_mM_dx_Id4 == 0:
							set_position(p_d, dC_AX_12p[1], dynamixel_id[1], b_tObj.pos_lh)

 		# show the result in the main frame
		cv2.imshow("Bioloid Humanoid", frame_mT)
		# ending condition
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
    # exit communication
	if s_p.close_serialPort():
		print('Serial port communication terminated.')

	# output
	return mult_t
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
