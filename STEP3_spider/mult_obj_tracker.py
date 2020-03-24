#########################################################################################################
# ============================== BRNO UNIVERSITY OF TECHNOLOGY ======================================== #
# ============================== FACULTY OF MECHANICAL ENGINEERING ==================================== #
# =========================INSITUTE OF AUTOMATION AND COMPUTER SCIENCE ================================ #
# Autor: Roman Parak
#########################################################################################################

import cv2
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Ellipse
import matplotlib as mpl
from matplotlib.collections import PatchCollection
import time
import math

import matplotlib  
matplotlib.use("TkAgg") # set the backend 

import communication
import dyn_ax_12p
import parameters

# init global var
global b, c
b = []
c = []

global r1P, r2P, r3P, r4P, r5P
r1P = patches.Rectangle((260, 160), 160, 160, facecolor='green', edgecolor='black')
r2P = patches.Rectangle((100, 160), 160, 160, facecolor='green', edgecolor='black')
r3P = patches.Rectangle((420, 160), 160, 160, facecolor='green', edgecolor='black')
r4P = patches.Rectangle((260, 320), 160, 160, facecolor='green', edgecolor='black')
r5P = patches.Rectangle((260, 0), 160, 160, facecolor='green', edgecolor='black')

def calculation(plt, fig, ax, x, y):
	global c 
	command  = calc_rectangle(ax, x, y)

	for _, a in enumerate(c):
		a.remove()
		c = []
		break

	#print(command)
	b = ax.annotate(command, xy=(430, 380),  xycoords='data',
		xytext=(10, 10), textcoords='offset points',
		size=35,
		bbox=dict(boxstyle="round", fc="0.8"))

	c.append(b)

	fig.canvas.draw()
	plt.show(block=False)
	return plt, command

def init():
	fig = plt.figure()
	ax  = fig.add_subplot(111)

	r1 = patches.Rectangle((260, 160), 160, 160, facecolor='None', edgecolor='black')
	r2 = patches.Rectangle((100, 160), 160, 160, facecolor='None', edgecolor='black')
	r3 = patches.Rectangle((420, 160), 160, 160, facecolor='None', edgecolor='black')
	r4 = patches.Rectangle((260, 320), 160, 160, facecolor='None', edgecolor='black')
	r5 = patches.Rectangle((260, 0), 160, 160, facecolor='None', edgecolor='black')

	plt.xlim(0, 640)
	plt.ylim(0, 480)

	# Major ticks every 20, minor ticks every 5
	major_ticksX = np.arange(0, 681, 20)
	minor_ticksX = np.arange(0, 681, 5)

	major_ticksY = np.arange(0, 481, 20)
	minor_ticksY = np.arange(0, 481, 5)


	ax.set_xticks(major_ticksX)
	ax.set_xticks(major_ticksX, minor=True)
	ax.set_yticks(major_ticksY)
	ax.set_yticks(minor_ticksY, minor=True)

	# And a corresponding grid
	ax.grid(which='both')

	# Or if you want different settings for the grids:
	ax.grid(which='minor', alpha=0.2)
	ax.grid(which='major', alpha=0.5)

	ax.add_patch(r1)
	ax.add_patch(r2)
	ax.add_patch(r3)
	ax.add_patch(r4)
	ax.add_patch(r5)

	return plt, fig, ax

def calc_rectangle(ax, x, y):
	command = ''
	if x > 260 and x < 420:
		if y > 0 and y < 160:
			r1P.set_visible(False)
			r2P.set_visible(False)
			r3P.set_visible(False)
			r4P.set_visible(False)
			r5P.set_visible(True)
			ax.add_patch(r5P)
			command = 'SIT_DOWN'
			#print('backwards')
		elif y > 160 and y < 320:
			r1P.set_visible(True)
			r2P.set_visible(False)
			r3P.set_visible(False)
			r4P.set_visible(False)
			r5P.set_visible(False)
			ax.add_patch(r1P)
			command = 'HOME'
			#print('HOME')
		elif y > 320 and y < 480:
			r1P.set_visible(False)
			r2P.set_visible(False)
			r3P.set_visible(False)
			r4P.set_visible(True)
			r5P.set_visible(False)
			ax.add_patch(r4P)
			command = 'STAND_UP'
			#print('forward')
	elif x > 100 and x < 260:
		if y > 160 and y < 320:
			r1P.set_visible(False)
			r2P.set_visible(True)
			r3P.set_visible(False)
			r4P.set_visible(False)
			r5P.set_visible(False)
			ax.add_patch(r2P)
			command = 'LEGS_RIGHT'
			#print('to the left')
	elif x > 420 and x < 580:
		if y > 160 and y < 320:
			r1P.set_visible(False)
			r2P.set_visible(False)
			r3P.set_visible(True)
			r4P.set_visible(False)
			r5P.set_visible(False)
			ax.add_patch(r3P)
			command = 'LEGS_LEFT'
			#print('to the right')
	else:
		print('nothing')

	return command
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
	# parameters for drawing {plot}
	COUNT_OF_OBJECTS = 2 # each color
	# identical to the frame size
	MIN_X = 0
	MAX_X = 640
	MIN_Y = 480
	MAX_Y = 0

	plt, fig, ax = init()
	fig.set_size_inches(12.5, 9.5) 
	fig.canvas.manager.window.wm_geometry("+%d+%d" % (0, 0))
	ax.set_title('Bioloid King-Spider {opencv control}', fontsize=14, fontweight='bold')
	ax.set_xlabel('Dimension X', fontsize=10, fontweight='bold')
	ax.set_ylabel('Dimension Y', fontsize=10, fontweight='bold')
    # x,y limitation

	# HSV - coordinates of the detected object
	lower_hsv = {
        'green':(17, 71, 78),
	} 

	upper_hsv = {
        'green':(27, 255, 255),
	}
	# initialization colors for ectangle around the object
	
	# initialization colors for circle and rectangle around the object
	colors_cr = {
		'green':(0,255,0),
	}

	# start recording
	mult_t = cv2.VideoCapture(device)

	if not(mult_t.isOpened()):
		mult_t.open(device)

	# set frame parameters
	mult_t.set(frame_width, 640)
	mult_t.set(frame_height, 480)

	port_name = 'COM4'
	p_d = parameters.param_dyn(port_name)

	# serial port communication
	s_p = communication.Serial_Port(p_d.PORT_NAME, p_d.BAUDRATE)

	# controll dynamixel AX-12+
	dynamixel_id = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
	dC_AX_12p    = []


	for init_d in range(0, len(dynamixel_id)):
		# initial AX-12+
		aux_dyn = dyn_ax_12p.dynamixel_AX12P(dynamixel_id[init_d], s_p.serial_port)
		dC_AX_12p.append(aux_dyn)

	
	# call functions {write}
	goal_speed = 50
	for i_speed in range(0, len(dC_AX_12p)):
		set_speed(p_d, dC_AX_12p[i_speed], dynamixel_id[i_speed], goal_speed)

	# dynamixel


	g_H = []
	count_g_H = 0
	position_state_H = 0

	g_F = []
	count_g_F = 0
	position_state_F = 0

	g_B = []
	count_g_B = 0
	position_state_B = 0

	g_TL = []
	count_g_TL = 0
	position_state_TL = 0

	g_TR = []
	count_g_TR = 0
	position_state_TR = 0

	goal_pos = [459, 575, 444, 590, 513, 512, 514, 514, 592, 422, 504, 457, 532, 369, 605, 411, 526, 441]

	# initialization approx. param
	green_approx_x  = 0
	green_approx_y  = 0
	command = ''
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
				# calculation object perimeter
				obj_perimeter = cv2.arcLength(obj_contour, True)
				approx        = cv2.approxPolyDP(obj_contour, 0.02 * obj_perimeter, True)
				if 6 < len(approx) < 15:
					# calculation area of the object
					obj_area = cv2.contourArea(obj_contour)
					# calculation circularity: formula {4 * pi * Area/(perimeter^2)}
					obj_circ = ((4 * math.pi * obj_area)/(obj_perimeter * obj_perimeter))
	
				    # condition of size {area} -> object
					if (50 < obj_area < 3000) and (0.3 < obj_circ < 1.5): 
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
	

						if color_k == 'green':
							if abs(green_approx_x - int(x_r)) <= 1 or abs(green_approx_y - int(x_r)) <= 1:
								plt, command = calculation(plt, fig, ax, green_approx_x, 480 - green_approx_y)
							else:
								green_approx_x = int(x_r)
								green_approx_y = int(y_r)

						if command == 'SIT_DOWN':
							goal_pos = [381, 648, 227, 826, 283, 742, 523, 498, 818, 211, 786, 269, 656, 349, 779, 250, 725, 293]

							for i_pos in range(0, len(dC_AX_12p)):
								set_position(p_d, dC_AX_12p[i_pos], dynamixel_id[i_pos], goal_pos[i_pos])
							print('1')
						elif command == 'HOME':
							goal_pos = [459, 575, 444, 590, 513, 512, 514, 514, 592, 422, 504, 457, 532, 369, 605, 411, 526, 441]

							for i_pos in range(0, len(dC_AX_12p)):
								set_position(p_d, dC_AX_12p[i_pos], dynamixel_id[i_pos], goal_pos[i_pos])

							print('2')
						elif command == 'STAND_UP':
							goal_pos = [507, 534, 649, 367, 638, 344, 508, 469, 292, 634, 303, 651, 585, 358, 373, 633, 385, 636]

							for i_pos in range(0, len(dC_AX_12p)):
								set_position(p_d, dC_AX_12p[i_pos], dynamixel_id[i_pos], goal_pos[i_pos])

							print('3')
						elif command == 'LEGS_RIGHT':
							goal_pos = [459, 575, 319, 589, 764, 512, 491, 413, 591, 422, 505, 457, 631, 369, 719, 411, 304, 440]

							for i_pos in range(0, len(dC_AX_12p)):
								set_position(p_d, dC_AX_12p[i_pos], dynamixel_id[i_pos], goal_pos[i_pos])

							print('4')
						elif command == 'LEGS_LEFT':
							goal_pos = [459, 575, 443, 719, 511, 322, 581, 560, 606, 421, 504, 456, 632, 369, 605, 321, 526, 701]

							for i_pos in range(0, len(dC_AX_12p)):
								set_position(p_d, dC_AX_12p[i_pos], dynamixel_id[i_pos], goal_pos[i_pos])

							print('5')



		# show the result in the main frame
		cv2.imshow("Multiple object tracker {Main frame}", frame_mT)

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
