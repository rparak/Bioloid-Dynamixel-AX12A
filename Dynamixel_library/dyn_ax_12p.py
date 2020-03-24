# import libraries
import struct
import math
class dynamixel_AX12P(object):
	def __init__(self, dynamixel_id, serial_port):
		# intialization parameters
		self.id    = dynamixel_id
		self._s_p  = serial_port 
		# packet initialization
		self.packet_param       = []
		self.packet_instruction = None
		self.packet_length      = None
		self.packet_check_sum   = None
		self.main_packet        = None
		# error detection
		self.err                = None
		# packet resutl
		self.result 			= None
		self.status_packet      = None
	def init_packet_param_AX_12p(self,init_packet_param):
		if init_packet_param[1] > 1:
			if init_packet_param[1] >= 0 and init_packet_param[1] <= 1023:
				# calculation command
				packet_real_part  = ((init_packet_param[1] - math.floor(init_packet_param[1]/256)*256)%256) # real part in the packet 
				packet_num_of_rot = math.floor(init_packet_param[1]/256); # number of packet rotation
				
				self.packet_param = [init_packet_param[0], packet_real_part, packet_num_of_rot]
			else:
				self.err = 1
				print('Command is out of range!')
		else:
			self.packet_param = [init_packet_param[0], init_packet_param[1]]
	def command_to_AX_12p(self,command):
		# set packet parameters
		self.packet_instruction = command # read or write
		self.packet_length      = len(self.packet_param) + 2
		self.packet_check_sum   = 255 - sum([self.id, self.packet_length, self.packet_instruction, sum(self.packet_param)])%256
		if len(self.packet_param) > 2:
			self.main_packet = bytearray([0xff, 0xff, self.id, self.packet_length, self.packet_instruction, self.packet_param[0], self.packet_param[1],self.packet_param[2], self.packet_check_sum])
		else:
			self.main_packet = bytearray([0xff, 0xff, self.id, self.packet_length, self.packet_instruction, self.packet_param[0], self.packet_param[1], self.packet_check_sum])

		try:
			# write packet
			self._s_p.write(self.main_packet)

			#print('Packet:' + ".".join("{:08b}".format(c) for c in packet))
			#print('Packet:' + ".".join("{:02x}".format(c) for c in packet))
		except OSError as v:
			if v.errno != errno.EAGAIN:
				raise SerialException('Write failed: %s' % (v,))

		# packet readline 
		self.status_packet = self._s_p.readline()
		#print('Status packet:' + ".".join("{:02x}".format(c) for c in status_p))

		# error detection
		self.__err_detect(self.status_packet)

		if command == 2:
			if self.packet_param[1] == 1:
				try:
					self.result = int(self.status_packet[5])
				except IndexError:
					self.result = 0
			else:
				self.result = str((self.status_packet[6] + 1)*(256) - (256 - self.status_packet[5]))

	def release_packet_param_AX_12p(self):
		# packet parameters
		self.packet_param       = []
		self.packet_instruction = None
		self.packet_length      = None
		self.packet_check_sum   = None
		self.main_packet        = None
		# error 
		self.err 				= None
		# packet resutlt
		self.result 			= None
		self.status_packet      = None
	def __err_detect(self, packet):
		# initialial error state
		err_state = 7
		# detect error packet
		err_p = packet[4:5]
		# transfer error packet hex to binary {out = string}
		err_p_bin = ''.join("{:08b}".format(c) for c in err_p)

		for i in range(0,len(err_p_bin)):
			if err_p_bin[i] == '1':
				err_state = i
				break
			else:
				err_state = 7

		e_states = {
		    0: 'Input Voltage Error { Set to 1 if the voltage is out of the operating voltage range as defined in the control table. }',
		    1: 'Angle Limit Error { Set as 1 if the Goal Position is set outside of the range between CW Angle Limit and CCW Angle Limit. }',
		    2: 'Overheating Error { Set to 1 if the internal temperature of the Dynamixel unit is above the operating temperature range as defined in the control table. }',
		    3: 'Range Error { Set to 1 if the instruction sent is out of the defined range. }',
		    4: 'Checksum Error { Set to 1 if the checksum of the instruction packet is incorrect }',
		    5: 'Overload Error { Set to 1 if the specified maximum torque can"t control theapplied load. }',
		    6: 'Instruction Error { Set to 1 if an undefined instruction is sent or an action instruction is sent without a Reg_Write instruction. }',
		    7: '-'
		}


		if err_state != 7:
			print(e_states.get(err_state, 'default'))
		else:
			self.err = 1