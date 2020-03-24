import sys
import communication
import dyn_ax_12p
import parameters
import time

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
# ========================================== MAIN ============================================ #
def main(argv=sys.argv):
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
	goal_speed = 75
	for i_speed in range(0, len(dC_AX_12p)):
		set_speed(p_d, dC_AX_12p[i_speed], dynamixel_id[i_speed], goal_speed)

	# home pos 
	goal_pos = [459,575,444,590,513,512,581,414,592,422,504,457,632,369,605,411,526,441]

	goal_posTRGH = [[372,610,267,512,268,512,512,509,536,256,510,291,650,364,739,513,735,523], [372,734,267,512,268,512,611,509,536,256,510,291,650,405,739,513,735,523],
			        [372,734,494,750,495,733,611,509,764,495,763,483,650,405,517,253,522,259], [372,655,494,750,495,733,519,509,764,495,763,483,650,329,517,253,522,259]]

	goal_posTLFT = [[414,652,512,757,512,756,515,512,760,480,733,514,660,374,511,285,501,289], [290,652,512,757,512,756,515,413,760,480,733,514,619,374,511,285,501,289],
			        [290,652,274,530,291,529,515,413,521,252,541,261,619,374,771,507,765,502], [369,652,274,530,291,529,515,505,521,252,541,261,695,374,771,507,765,502]]

	goal_posWFWD = [[458,584,469,767,517,733,326,569,803,414,729,411,581,443,490,236,596,410], [429,575,521,739,431,610,489,730,801,390,741,412,585,447,617,203,551,307],
			        [440,566,257,555,291,507,455,698,602,213,613,289,581,443,788,534,614,428], [449,595,285,503,414,593,294,535,626,215,612,274,577,439,821,407,717,473]]

	goal_posWBKW = [[458,584,469,767,517,733,326,569,803,414,729,411,581,443,490,236,596,410], [449,595,285,503,414,593,294,535,626,215,612,274,577,439,821,407,717,473],
			        [440,566,257,555,291,507,455,698,602,213,613,289,581,443,788,534,614,428], [429,575,521,739,431,610,489,730,801,390,741,412,585,447,617,203,551,307]]

	for i_pos in range(0, len(dC_AX_12p)):
		set_position(p_d, dC_AX_12p[i_pos], dynamixel_id[i_pos], goal_pos[i_pos])

	g = []
	count_g = 0
	position_state = 0
	while 1:
		for i_presPos in range(0, len(dC_AX_12p)):
			a = is_motor_moving(p_d, dC_AX_12p[i_presPos], dynamixel_id[i_presPos])
			g.append(a)

		for i_g in range(0, len(dC_AX_12p)):
			if g[i_g] == 0:
				count_g += 1

		g = []

		if count_g == 18:
			# call functions {write}
			goal_speed = 600
			for i_speed in range(0, len(dC_AX_12p)):
				set_speed(p_d, dC_AX_12p[i_speed], dynamixel_id[i_speed], goal_speed)

			goal_pos = goal_pos[position_state]
			for i_pos in range(0, len(dC_AX_12p)):
				set_position(p_d, dC_AX_12p[i_pos], dynamixel_id[i_pos], goal_pos[i_pos])

			if position_state == 3:
				position_state = 0
			else:
				position_state += 1
		else:
			print(count_g)

		count_g = 0


	# exit communication
	if s_p.close_serialPort():
		print('Serial port communication terminated.')

# ======================================== CALL MAIN ========================================== #
if __name__ == "__main__":
    sys.exit(main())