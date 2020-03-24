#########################################################################################################
# ============================== BRNO UNIVERSITY OF TECHNOLOGY ======================================== #
# ============================== FACULTY OF MECHANICAL ENGINEERING ==================================== #
# =========================INSITUTE OF AUTOMATION AND COMPUTER SCIENCE ================================ #
# Autor: Roman Parak
#########################################################################################################

import sys
import communication
import dyn_ax_12p
import parameters

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
# ========================================== MAIN ============================================ #
def main(argv=sys.argv):
	# dynamixel parameters for communication {initialization}
	port_name = 'COM5'
	p_d = parameters.param_dyn(port_name)

	# serial port communication
	s_p = communication.Serial_Port(p_d.PORT_NAME, p_d.BAUDRATE)

	# controll dynamixel AX-12+
	dynamixel_id = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
	dC_AX_12p    = []
	#dynamixel_id = [3, 4]

	for init_d in range(0, len(dynamixel_id)):
		# initial AX-12+
		aux_dyn = dyn_ax_12p.dynamixel_AX12P(dynamixel_id[init_d], s_p.serial_port)
		dC_AX_12p.append(aux_dyn)

	#for i_temp in range(0, len(dC_AX_12p)):
		# call functions {read}
		#present_temperature(p_d, dC_AX_12p[i_temp], dynamixel_id[i_temp])
	
	# call functions {write}
	goal_speed = 300
	for i_speed in range(0, len(dC_AX_12p)):
		set_speed(p_d, dC_AX_12p[i_speed], dynamixel_id[i_speed], goal_speed)

	goal_pos = [204, 818, 250, 770, 512, 512, 358, 666, 512, 512, 444, 578, 375, 646, 599, 423, 512, 512]
	#goal_pos = [500, 500]

	for i_pos in range(0, len(dC_AX_12p)):
		set_position(p_d, dC_AX_12p[i_pos], dynamixel_id[i_pos], goal_pos[i_pos])


	"""
	counter_1 = 0
	while counter_1 < len(goal_pos):
		set_position(p_d, dC_AX_12p[init_d], dynamixel_id[counter_1], goal_pos[counter_1])
		is_mM = is_motor_moving(p_d, dC_AX_12p[init_d], dynamixel_id[counter_1])

		if is_mM == 0:
			counter_1 = counter_1 + 1
	"""
	# exit communication
	if s_p.close_serialPort():
		print('Serial port communication terminated.')

# ======================================== CALL MAIN ========================================== #
if __name__ == "__main__":
    sys.exit(main())
