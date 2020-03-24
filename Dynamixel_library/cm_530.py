import serial
import sys
import struct
import math


# ======================================= INIT SERIAL PORT =================================== #
def init_serial(port):
	return serial.Serial(
		port      = port,
		baudrate  = 1000000,
		bytesize  = serial.EIGHTBITS,
		parity    = serial.PARITY_NONE,
		stopbits  = serial.STOPBITS_ONE,
		timeout   = 0.01,
		xonxoff   = False,
        rtscts    = False,
        dsrdtr    = False
		)
# ========================================== READ ============================================ #
def present_temperature(serial_port,id_d):
	packet_length = 4
	instruction   = 2  # read
	param_1       = 43 
	param_2       = 1
	check_sum     = 255 - ((id_d + packet_length + instruction + param_1 + param_2)%256) 

	packet 	      = bytearray([0xff, 0xff, id_d, packet_length, instruction, param_1, param_2, check_sum])

	print('Packet:' + ".".join("{:08b}".format(c) for c in packet))
	print('Packet:' + ".".join("{:02x}".format(c) for c in packet))

	serial_port.write(packet)

	status_p = serial_port.readline()
	print('Status packet:' + ".".join("{:02x}".format(c) for c in status_p))

	return str(status_p[5])
def is_moving(serial_port,id_d):
	packet_length = 4
	instruction   = 2  # read
	param_1       = 46 
	param_2       = 1

	check_sum     = 255 - ((id_d + packet_length + instruction + param_1 + param_2)%256) 

	packet 	      = bytearray([0xff, 0xff, id_d, packet_length, instruction, param_1, param_2, check_sum])

	print('Packet:' + ".".join("{:08b}".format(c) for c in packet))
	print('Packet:' + ".".join("{:02x}".format(c) for c in packet))

	serial_port.write(packet)
	status_p = serial_port.readline()
	print('Status packet:' + ".".join("{:02x}".format(c) for c in status_p))

	return str(status_p[5])
def present_position(serial_port,id_d):
	packet_length = 4
	instruction   = 2 # read
	param_1       = 36 
	param_2       = 2 
	check_sum     = 255 - ((id_d + packet_length + instruction + param_1 + param_2)%256) 

	packet 	      = bytearray([0xff, 0xff, id_d, packet_length, instruction, param_1, param_2, check_sum])
	
	print('Packet:' + ".".join("{:08b}".format(c) for c in packet))
	print('Packet:' + ".".join("{:02x}".format(c) for c in packet))

	serial_port.write(packet)

	status_p = serial_port.readline()
	print('Status packet:' + ".".join("{:02x}".format(c) for c in status_p))

	return str((status_p[6] + 1)*(256) - (256 - status_p[5]))
def present_speed(serial_port,id_d):
	packet_length = 4
	instruction   = 2 # read
	param_1       = 38
	param_2       = 2 
	check_sum     = 255 - ((id_d + packet_length + instruction + param_1 + param_2)%256) 

	packet 	      = bytearray([0xff, 0xff, id_d, packet_length, instruction, param_1, param_2, check_sum])

	print('Packet:' + ".".join("{:08b}".format(c) for c in packet))
	print('Packet:' + ".".join("{:02x}".format(c) for c in packet))

	serial_port.write(packet)
	status_p = serial_port.readline()
	print('Status packet:' + ".".join("{:02x}".format(c) for c in status_p))

	return str((status_p[6] + 1)*(256) - (256 - status_p[5]))
# ========================================== WRITE ============================================ #
def led_on_off(serial_port, id_d, state):

	if state == 'on':
		# led on
		packet_length = 4
		instruction   = 3 
		param_1       = 25 
		param_2       = 1 
		check_sum     = 255 - ((id_d + packet_length + instruction + param_1 + param_2)%256) 
	elif state == 'off':
		# led off
		packet_length = 4
		instruction   = 3 
		param_1       = 25 
		param_2       = 0 
		check_sum     = 255 - ((id_d + packet_length + instruction + param_1 + param_2)%256) 

	packet = bytearray([0xff, 0xff, id_d, packet_length, instruction, param_1, param_2, check_sum]) 

	print('Packet:' + ".".join("{:08b}".format(c) for c in packet))
	print('Packet:' + ".".join("{:02x}".format(c) for c in packet))
	serial_port.write(packet)

	status_p = serial_port.readline()
	print('Status packet:' + ".".join("{:02x}".format(c) for c in status_p))
def goal_position(serial_port, id_d, goal_pos):
	if goal_pos >= 0 and goal_pos <= 1023: 
		# multiple packet for goal position
		packet_gp_real_pP    = ((goal_pos - math.floor(goal_pos/256)*256)%256) # real position in the packet
		packet_gp_num_of_rot = math.floor(goal_pos/256); # number of packet rotation

		packet_length = 5
		instruction   = 3 # write
		param_1       = 30 # write goal position
		check_sum     = 255 - ((id_d + packet_length + instruction + param_1 + packet_gp_real_pP + packet_gp_num_of_rot)%256)

		packet = bytearray([0xff, 0xff, id_d, packet_length, instruction, param_1, packet_gp_real_pP, packet_gp_num_of_rot, check_sum])

		print('Packet:' + ".".join("{:08b}".format(c) for c in packet))
		print('Packet:' + ".".join("{:02x}".format(c) for c in packet))

		serial_port.write(packet)

		status_p = serial_port.readline()
		print('Status packet:' + ".".join("{:02x}".format(c) for c in status_p))
	else:
		print('Position is out of range!')

def moving_speed(serial_port, id_d, moving_s):
	if moving_s >= 0 and moving_s <= 1023: 
		# multiple packet for goal position
		packet_ms_real_pP    = ((moving_s - math.floor(moving_s/256)*256)%256) # real position in the packet
		packet_ms_num_of_rot = math.floor(moving_s/256); # number of packet rotation

		packet_length = 5
		instruction   = 3 # write
		param_1       = 32 # write moving speed
		check_sum     = 255 - ((id_d + packet_length + instruction + param_1 + packet_ms_real_pP + packet_ms_num_of_rot)%256)

		packet = bytearray([0xff, 0xff, id_d, packet_length, instruction, param_1, packet_ms_real_pP, packet_ms_num_of_rot, check_sum])

		print('Packet:' + ".".join("{:08b}".format(c) for c in packet))
		print('Packet:' + ".".join("{:02x}".format(c) for c in packet))

		serial_port.write(packet)

		status_p = serial_port.readline()
		print('Status packet:' + ".".join("{:02x}".format(c) for c in status_p))
	else:
		print('Speed is out of range!')

# ========================================== MAIN ============================================ #
def main(argv):
	try:
		# initialization of serial communication
		port_name   = 'COM5'
		serial_port = init_serial(port_name)

		if serial_port.isOpen():
			print('Open serial port: '+ serial_port.name)
		else:
			print('Not open!')
	except:
		print('Error!')
		exit()

	# initilaziation dynamixel ID
	dynamixel_id  = 1

	# read temperature
	temp_r = present_temperature(serial_port, dynamixel_id)
	print('Present temperature:' + temp_r)

	# read position
	pos_r  = present_position(serial_port,dynamixel_id)
	print('Present position:' + pos_r)

	# read speed
	speed_r = present_speed(serial_port,dynamixel_id)
	print('Present speed:' + speed_r)

	# turn on/off LED
	led_on_off(serial_port, dynamixel_id, 'off')

	# set{write} moving speed
	moving_s = 0
	#moving_speed(serial_port, dynamixel_id, moving_s)

	# set{write} goal position
	goal_pos = 512
	#goal_position(serial_port, dynamixel_id, goal_pos)


	while True:
		# read motor movement
		moving_m = is_moving(serial_port,dynamixel_id)
		if moving_m == '1':
			print('Motor moving:' + moving_m)
		else:
			print('Motor moving:' + moving_m)
			break

	serial_port.close()

# ======================================== CALL MAIN ========================================== #
if __name__ == "__main__":
    main(sys.argv)