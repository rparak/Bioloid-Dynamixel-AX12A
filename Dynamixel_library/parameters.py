class param_dyn(object):
	def __init__(self, port):
		# SERIAL PORT 
		self.PORT_NAME = port
		self.BAUDRATE  = 1000000 # Tolerance = 0,000%
		# AREA {EEPROM} | ADDRESS {DECIMAL} | NAME | DESCRIPTION | ACCESS    
		self.AX_12p_MODEL_NUMBER_L     = 0 # Lowest byte of model number {R}
		self.AX_12p_MODEL_NUMBER_H     = 1 # Highest byte of model number {R}
		self.AX_12p_VERSION            = 2 # Information on the version of firmware {R}
		self.AX_12p_ID                 = 3 # ID of Dynamixel {RW}
		self.AX_12p_BAUD_RATE          = 4 # Baud Rate of Dynamixel {RW}
		self.AX_12p_RETURN_DELAY_TIME  = 5 # Return Delay Time {RW}
		self.AX_12p_CW_ANGLE_LIMIT_L   = 6 # Lowest byte of clockwise Angle Limit {RW}
		self.AX_12p_CW_ANGLE_LIMIT_H   = 7 # Highest byte of clockwise Angle Limit {RW}
		self.AX_12p_CCW_ANGLE_LIMIT_L  = 8 # Lowest byte of counterclockwise Angle Limit{RW}
		self.AX_12p_CCW_ANGLE_LIMIT_H  = 9 # Highest byte of counterclockwise Angle Limit {RW}
		self.AX_12p_LIMIT_TEMPERATURE  = 11 # Internal Limit Temperature {RW}
		self.AX_12p_DOWN_LIMIT_VOLTAGE = 12 # Lowest Limit Voltage {RW}
		self.AX_12p_UP_LIMIT_VOLTAGE   = 13 # Highest Limit Voltage {RW}
		self.AX_12p_MAX_TORQUE_L       = 14 # Lowest byte of Max. Torque {RW}
		self.AX_12p_MAX_TORQUE_H       = 15 # Highest byte of Max. Torque {RW}
		self.AX_12p_RETURN_LEVEL       = 16 # Status Return Level {RW}
		self.AX_12p_ALARM_LED          = 17 # LED for Alarm RW}
		self.AX_12p_ALARM_SHUTDOWN     = 18 # Shutdown for Alarm {RW}
		# AREA {RAM} | ADDRESS {DECIMAL} | NAME | DESCRIPTION | ACCESS 
		self.AX_12p_TORQUE_ENABLE          = 24 # Torque On/Off {RW}
		self.AX_12p_LED                    = 25 # LED On/Off {RW}
		self.AX_12p_CW_COMPLIANCE_MARGIN   = 26 # CW Compliance margin {RW}
		self.AX_12p_CCW_COMPLIANCE_MARGIN  = 27 # CCW Compliance margin {RW}
		self.AX_12p_CW_COMPLIANCE_SLOPE    = 28 # CW Compliance slope {RW}
		self.AX_12p_CCW_COMPLIANCE_SLOPE   = 29 # CCW Compliance slope
		self.AX_12p_GOAL_POSITION_L        = 30 # Lowest byte of Goal Position {RW}
		self.AX_12p_GOAL_POSITION_H        = 31 # Highest byte of Goal Position {RW}
		self.AX_12p_GOAL_SPEED_L           = 32 # Lowest byte of Moving Speed (Moving Velocity) {RW}
		self.AX_12p_GOAL_SPEED_H           = 33 # Highest byte of Moving Speed (Moving Velocity) {RW}
		self.AX_12p_TORQUE_LIMIT_L         = 34 # Lowest byte of Torque Limit (Goal Torque) {RW}
		self.AX_12p_TORQUE_LIMIT_H         = 35 # Highest byte of Torque Limit (Goal Torque) {RW}
		self.AX_12p_PRESENT_POSITION_L     = 36 # Lowest byte of Current Position (Present Position) {R}
		self.AX_12p_PRESENT_POSITION_H     = 37 # Highest byte of Current Position (Present Position) {R}
		self.AX_12p_PRESENT_SPEED_L        = 38 # Lowest byte of Current Speed {R}
		self.AX_12p_PRESENT_SPEED_H        = 39 # Highest byte of Current Speed {R}
		self.AX_12p_PRESENT_LOAD_L         = 40 # Lowest byte of Current Load {R}
		self.AX_12p_PRESENT_LOAD_H         = 41 # Highest byte of Current Load {R}
		self.AX_12p_PRESENT_VOLTAGE        = 42 # Current Voltage {R}
		self.AX_12p_PRESENT_TEMPERATURE    = 43 # Current Temperature {R}
		self.AX_12p_REGISTERED_INSTRUCTION = 44 # Means if Instruction is registered {R}
		self.AX_12p_MOVING                 = 46 # Means if there is any movement {R}
		self.AX_12p_LOCK                   = 47 # Locking EEPROM {RW}
		self.AX_12p_PUNCH_L                = 48 # Lowest byte of Punch {RW}
		self.AX_12p_PUNCH_H                = 49 # Highest byte of Punch {RW}
		# STATUS RETURNS LEVELS | NAME | VALUE | DESCRIPTION
		self.AX_12p_RETURN_NONE = 0 # No return against all commands (Except PING Command)
		self.AX_12p_RETURN_READ = 1 # Return only for the READ command
		self.AX_12p_RETURN_ALL  = 2 # Return for all commands
    	# INSTRUCTION SET | NAME | VALUE | FUNCTION 
		self.AX_12p_PING       = 1 # No action. Used for obtaining a Status Packet
		self.AX_12p_READ_DATA  = 2 # Reading values in the Control Table 
		self.AX_12p_WRITE_DATA = 3 # AX_12p_WRITE_DATAriting values to the Control Table
		self.AX_12p_REG_WRITE  = 4 # Similar to WRITE_DATA, but stays in standby mode until the ACION instruction is given
		self.AX_12p_ACTION     = 5 # Triggers the action registered by the REG_WRITE instruction
		self.AX_12p_RESET      = 6 # Changes the control table values of the Dynamixel actuator to the Factory Default Value settings
		self.AX_12p_SYNC_WRITE = 131 # Used for controlling many Dynamixel actuators at the same time