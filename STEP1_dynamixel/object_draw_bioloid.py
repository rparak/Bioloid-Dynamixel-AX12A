#########################################################################################################
# ============================== BRNO UNIVERSITY OF TECHNOLOGY ======================================== #
# ============================== FACULTY OF MECHANICAL ENGINEERING ==================================== #
# =========================INSITUTE OF AUTOMATION AND COMPUTER SCIENCE ================================ #
# Autor: Roman Parak
#########################################################################################################

import matplotlib.pyplot as plt
import matplotlib.patches as mpatch
import matplotlib.lines as mline
import numpy as np
import math

import matplotlib  
matplotlib.use("TkAgg") # set the backend  

class tracking_bioloid(object):
    def __init__(self, green_point, blue_point):
        # figure
        self._figure = plt.figure()
        self._figure.set_size_inches(12.5, 9.5) 
        self._figure.canvas.manager.window.wm_geometry("+%d+%d" % (0, 0))
        self._axis   = self._figure.add_subplot(111)
        self._plot   = plt
        self._labels = ('Position', 'Velocity')

        self.rect_vel = self._axis.add_patch(mpatch.Rectangle((100, 0), 80, 380, fill=None, alpha=1))
        self.rect_pos = self._axis.add_patch(mpatch.Rectangle((500, 0), 80, 380, fill=None, alpha=1))
        # variables for legend
        self.c_vel = 0
        self.c_pos = 0
    def axis_init(self, x_limit, y_limit):
        # font
        font = {'family': 'TSTAR PRO',
        'color':  'black',
        'weight': 'normal',
        'size': 30,
        }

        font2 = {'family': 'TSTAR PRO',
        'color':  'black',
        'weight': 'normal',
        'size': 25,
        }
        # initialization parameters
        x = []
        y = []
        # set window setting {title, labels, limitations}
        self._axis.set_title('Dynamixel AX-12A {opencv control}', fontsize=14, fontweight='bold')


        # x, y label
        self._axis.set_xlabel('Dimension X', fontsize=10, fontweight='bold')
        self._axis.set_ylabel('Dimension Y', fontsize=10, fontweight='bold')
        # x,y limitation
        self._axis.set_xlim(0, x_limit)
        self._axis.set_ylim(0, y_limit)

        # turn on ticks for edit {major, minor}
        major_ticksX = np.arange(0, 681, 20)
        minor_ticksX = np.arange(0, 681, 5)

        major_ticksY = np.arange(0, 481, 20)
        minor_ticksY = np.arange(0, 481, 5)

        self._axis.set_xticks(major_ticksX)
        self._axis.set_xticks(major_ticksX, minor=True)
        self._axis.set_yticks(major_ticksY)
        self._axis.set_yticks(minor_ticksY, minor=True)

        self._axis.grid(which='both')

        # edit the major grid
        self._axis.grid(which='minor', alpha=0.2)
        # edit the minor grid
        self._axis.grid(which='major', alpha=0.5)

        # global
        global rec_pos, rec_vel
        self.rec_vel = self._axis.add_patch(mpatch.Rectangle((100, 0), 80, 380, fill=None, alpha=1))
        self.rec_pos = self._axis.add_patch(mpatch.Rectangle((500, 0), 80, 380, fill=None, alpha=1))

        # text
        self._plot.text(200, 320, r'Institute of Automation', fontdict=font)
        self._plot.text(200, 260, r'and Computer Science', fontdict=font)
        self._plot.text(200, 180, r'http://uai.fme.vutbr.cz/en/', fontdict=font2)
        # open figure
        self._figure.canvas.draw()
        self._plot.show(block=False)
    def control_rect(self, command_pos, command_vel):

        if self.c_vel != command_vel and command_vel <= 380:
            if self.rect_vel:
                self.rect_vel.remove()

            self.rect_vel = self._axis.add_patch(mpatch.Rectangle((100, 0), 80, command_vel, ec="black", facecolor='#66b5ff'))

            self.c_vel = command_vel

        if self.c_pos != command_pos and command_pos <= 380:
            if self.rect_pos:
                self.rect_pos.remove()

            self.rect_pos = self._axis.add_patch(mpatch.Rectangle((500, 0), 80, command_pos, ec="black", facecolor='#c1ff66'))

            self.c_pos = command_pos


        global vel, pos

        vel = self.rect_vel
        pos = self.rect_pos

        self._axis.legend([pos, vel], self._labels, loc='upper right', labelspacing= 1, fontsize=20)

        self._figure.canvas.draw()
    def plot_block_show(self):
        self._plot.show(block=True)
        
        
        
    
