#########################################################################################################
# ============================== BRNO UNIVERSITY OF TECHNOLOGY ======================================== #
# ============================== FACULTY OF MECHANICAL ENGINEERING ==================================== #
# =========================INSITUTE OF AUTOMATION AND COMPUTER SCIENCE ================================ #
# Autor: Roman Parak
#########################################################################################################

import pylab
from pylab import *
import sys
import communication
import dyn_ax_12p
import parameters
import time

from tkinter import *
import time
import threading

class HSV_init_scale:
    def __init__(self):
        self.Position = 0
        self.Velocity = 0

def init_current_scale(root, hsv_var, label):
    return Scale(root, from_=0, to=500, length=500, tickinterval=50, orient=HORIZONTAL, label=label, command=lambda v: setattr(scale_hsv, hsv_var, v))
def main_loop_scale(scale):
    root=Tk()
    root.title('Dynamixel AX-1A - Manual control')
    hsv_var = ['Position','Velocity']
    
    s   = []
    hsv = [0, 0]
    for i in range(0,len(hsv_var)):
        s = init_current_scale(root, hsv_var[i], hsv_var[i])
        s.set(hsv[i])
        s.pack()

    root.mainloop()

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

# define global class for scale
global scale_hsv
# initialization class for scale
scale_hsv = HSV_init_scale()

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

goal_speed = 50
for i_speed in range(0, len(dC_AX_12p)):
  set_speed(p_d, dC_AX_12p[i_speed], dynamixel_id[i_speed], goal_speed)

# initialization x, y
xAchse=pylab.arange(0,100,1)
yAchse=pylab.array([0]*100)

# Axis - Position
fig = pylab.figure(1)
ax = fig.add_subplot(211)
ax.grid(True)
ax.set_title('Dynamixel AX-12A (Position)')
ax.set_xlabel("Time (s)")
ax.set_ylabel("Position (units)")
ax.axis([0,100,-100,500])
line1=ax.plot(xAchse,yAchse,'b-')

# Axis - Velocity
fig = pylab.figure(1)
ax1 = fig.add_subplot(212)
ax1.grid(True)
ax1.set_title('Dynamixel AX-12A (Velocity)')
ax1.set_xlabel("Time (s)")
ax1.set_ylabel("Velocity (units/s)")
ax1.axis([0,100,-100,500])
line2=ax1.plot(xAchse,yAchse,'r-')

# get current figure {manager}
manager = pylab.get_current_fig_manager()

i = 0
goal_pos = 10
values=[]
values1 = []
res = present_position(p_d, dC_AX_12p[0], dynamixel_id[0])
values = [0 for x in range(100)]
values1 = [0 for x in range(100)]

goal_speed = 50
res_before = present_position(p_d, dC_AX_12p[0], dynamixel_id[0])
res_beforeN = 0
pos_bR      = 0
pos_bL      = 240
pos_goalE1  = 0
goal_speed1 = 0

pos_forValue = 10

def control_servo(pos, vel):
  global res, res_before, res_beforeN, pos_bR, pos_bL

  res   = present_position(p_d, dC_AX_12p[0], dynamixel_id[0])
  set_speed(p_d, dC_AX_12p[0], dynamixel_id[0], vel)
  set_position(p_d, dC_AX_12p[0], dynamixel_id[0], pos)
  
  if res_before - 5 < res < res_before + 5:
    pass
  else:
    res_before = res
    #print(res)
    if pos == 240:
      if res_before < pos_bR:
        res_before = pos_bR

      if res_before > pos:
        res_before = pos

      pos_bR = res_before
    elif pos == 10:
      if 0 <= res_before <= 10:
        res_before = pos

      if res_before > pos_bL or res_before == 10:
        res_before = pos_bL

      pos_bL = res_before
      # 10 - 13
      # 237 - 240
  
  return res

# Sinwave Generator
def SinwaveformGenerator(arg):
  global values, values1, res_actualForV, pos_forValue
  global res, res_before, res_beforeN, pos_bR, pos_bL

  #res_actualForV = control_servo(int(scale_hsv.Position), int(scale_hsv.Velocity))

  #print(res_actualForV)
  res   = present_position(p_d, dC_AX_12p[0], dynamixel_id[0])
  set_speed(p_d, dC_AX_12p[i_speed], dynamixel_id[i_speed], int(scale_hsv.Velocity))
  set_position(p_d, dC_AX_12p[0], dynamixel_id[0], int(scale_hsv.Position))
  
  if res_before - 5 < res < res_before + 5:
    pass
  else:
    res_before = res
    #print(res)
    if int(scale_hsv.Position) == 240:
      if res_before < pos_bR:
        res_before = pos_bR

      if res_before > int(scale_hsv.Position):
        res_before = int(scale_hsv.Position)

      pos_bR = res_before
    elif int(scale_hsv.Position) == 10:
      if 0 <= res_before <= 10:
        res_before = int(scale_hsv.Position)

      if res_before > pos_bL or res_before == 10:
        res_before = pos_bL

      pos_bL = res_before
      # 10 - 13
      # 237 - 240

  print(res, res_before)
  values.append(int(scale_hsv.Position))
  values1.append(int(scale_hsv.Velocity))

# Real-time Ploter
def RealtimePloter(arg):
  global values, values1

  CurrentXAxis=pylab.arange(len(values)-100,len(values),1)
  line1[0].set_data(CurrentXAxis,pylab.array(values[-100:]))
  ax.axis([CurrentXAxis.min(),CurrentXAxis.max(),-100,500])

  CurrentXAxis2=pylab.arange(len(values1)-100,len(values1),1)
  line2[0].set_data(CurrentXAxis2,pylab.array(values1[-100:]))
  ax1.axis([CurrentXAxis2.min(),CurrentXAxis2.max(),-100,500])

  manager.canvas.draw()

# Initialization Timer
timer = fig.canvas.new_timer(interval=1)
timer.add_callback(RealtimePloter, ())
timer2 = fig.canvas.new_timer(interval=1)
timer2.add_callback(SinwaveformGenerator, ())
timer.start()
timer2.start()

# threading scale_loop
threading.Thread(target=main_loop_scale, args=(scale_hsv,)).start()

# Show actual result
pylab.show()

# Close port
s_p.close_serialPort()
