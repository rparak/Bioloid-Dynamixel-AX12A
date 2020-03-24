try:
    import serial
    import struct
except:
    print('This module requires the pySerial to be installed.')

class Serial_Port(object):
	def __init__(self,m_port,m_baudrate):
		try:
			self.serial_port = serial.Serial(
				port      = m_port,
				baudrate  = m_baudrate,
				bytesize  = serial.EIGHTBITS,
				parity    = serial.PARITY_NONE,
				stopbits  = serial.STOPBITS_ONE,
				timeout   = 0.01,
				xonxoff   = False,
		        rtscts    = False,
			    dsrdtr    = False
		    )

			if self.serial_port.isOpen():
				print('Open serial port: '+ self.serial_port.name)
			else:
				print('The port is in use.')
		except serial.SerialException:
			print('No serial port data available.')
			exit()
	def close_serialPort(self):
		self.serial_port.close()
		return 1
