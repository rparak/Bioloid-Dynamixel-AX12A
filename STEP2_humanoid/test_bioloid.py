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
	packet_command = [p_d.AX_12p_PRESENT_TEMPERATURE, p_d.AX_12p_RETURN_READ] # ARAME | STATUS RETURNS LEVELS

	dC_AX_12p.init_packet_param_AX_12p(packet_command)

	if dC_AX_12p.err == None:
		dC_AX_12p.command_to_AX_12p(p_d.AX_12p_READ_DATA) # INSTRUCTION SET
		#dC_AX_12p.command_to_AX_12p(p_d.AX_12p_WRITE_DATA) # INSTRUCTION SET

		# print result
		print('Present temperature: ' + dC_AX_12p.result)
		# release of variables
		dC_AX_12p.release_packet_param_AX_12p()
	else:
		print('Error!')


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
# ========================================== MAIN ============================================ #
def main(argv=sys.argv):
	# dynamixel parameters for communication {initialization}
	port_name = 'COM4'
	p_d = parameters.param_dyn(port_name)

	# serial port communication
	s_p = communication.Serial_Port(p_d.PORT_NAME, p_d.BAUDRATE)

	# controll dynamixel AX-12+
	dynamixel_id_1 = 1

	# initial AX-12+
	dC_AX_12p = dyn_ax_12p.dynamixel_AX12P(dynamixel_id_1, s_p.serial_port)

	# call functions
	present_temperature(p_d, dC_AX_12p, dynamixel_id_1)
	
	goal_pos = 512
	set_position(p_d, dC_AX_12p, dynamixel_id_1, goal_pos)

	# exit communication
	if s_p.close_serialPort():
		print('Serial port communication terminated.')

# ======================================== CALL MAIN ========================================== #
if __name__ == "__main__":
    sys.exit(main())
