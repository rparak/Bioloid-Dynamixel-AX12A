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
        self._labels = ('Dead zone', 'Left hand', 'Right hand')
        # variables for legend
        self._rect   = []
        self._tr1    = []
        self._tr2    = []
        # number of points
        self.num_of_c    = ['green', 'blue']
        self.num_of_p    = [green_point, blue_point]
        # annotate list for colors
        self._ann     = [[[], [], [], [], [], []], # annotate 1 - number of colors {row}, 1 - number of annotate {column}
                         [[], [], [], [], [], []], 
                         [[], [], [], [], [], []]]
        # triangle 1 {body}
        self._point_tr_1        = [[[340, 100]], [[340, 400]], [[340, 100]]] # point triangle {1 - 3}
        self._triangle_1        = []
        self._mpatch_triangle_1 = []
        # triangle 2 {body}
        self._point_tr_2        = [[[260, 100]], [[260, 400]], [[260, 100]]] # point triangle {1 - 3}
        self._triangle_2        = []
        self._mpatch_triangle_2 = []
        # drawing points
        self.b_c = []
        self.g_c = []
        # output {final results}
        self.angle_rh = 0
        self.angle_lh = 0
        self.pos_rh   = 0
        self.pos_lh   = 0
    def axis_init(self, x_limit, y_limit):
        # initialization parameters
        x = []
        y = []
        # set window setting {title, labels, limitations}
        self._axis.set_title('Bioloid Humanoid {opencv control}', fontsize=14, fontweight='bold')
        # x, y label
        self._axis.set_xlabel('Dimension X', fontsize=10, fontweight='bold')
        self._axis.set_ylabel('Dimension Y', fontsize=10, fontweight='bold')
        # x,y limitation
        self._axis.set_xlim(0, x_limit)
        self._axis.set_ylim(y_limit, 0)
        # turn on ticks for edit {major, minor}
        self._axis.minorticks_on()
        # edit the major grid
        self._axis.grid(which='major', linestyle='-', linewidth='0.5', color='black')
        # edit the minor grid
        self._axis.grid(which='minor', linestyle=':', linewidth='0.5', color='black')
        # initialization drawing points {with color(circle)}
        self.b_c = [self._axis.plot(x, y, 'o', color='blue', markersize=8)[0], self._axis.plot(x, y, 'o', color='blue', markersize=8)[0], self._axis.plot(x, y, 's', color='black', markersize=8)[0]]
        self.g_c = [self._axis.plot(x, y, 'o', color='green', markersize=8)[0], self._axis.plot(x, y, 'o', color='green', markersize=8)[0], self._axis.plot(x, y, 's', color='green', markersize=8)[0]]
        # draw rectangle
        global rect
        rect = self._axis.add_patch(mpatch.Rectangle((260, 100), 80, 300, ec="black", facecolor='#FF6666'))
        # open figure
        self._figure.canvas.draw()
        self._plot.show(block=False)
    def _init_color(self, com_color, obj_num):
        if com_color == 'blue':
            r_color = self.b_c[obj_num]
        if com_color == 'green':
            r_color = self.g_c[obj_num]

        return r_color
    def _draw_objects(self, x_c, y_c, obj_idx, col_idx, c_var):
        for _, a in enumerate(self._ann[obj_idx][col_idx]):
            a.remove()
            self._ann[obj_idx][col_idx][:] = []
            break
            
        #act_color.set_xdata(x_c)
        #act_color.set_ydata(y_c)

        #str_ann  = '[ ' + str(x_c) + ', ' + str(y_c) + ' ]'
        #init_ann = self._axis.annotate(str_ann, (x_c + c_var, y_c + 10), fontsize=8, fontweight='bold')
        #self._ann[obj_idx][col_idx].append(init_ann)
 
        self._figure.canvas.draw()
    def _draw_triangle_no1(self, x, y):
         # collection of data for drawing triangle
        if self._point_tr_1[2]:
                self._point_tr_1[2] = []
                self._point_tr_1[2].append([x,y])
            
        # number of points
        for i in range(0, 3):
            self._triangle_1.append(self._point_tr_1[i][0])
            
        if len(self._triangle_1) == 3:
            # drawing triangle {robot body}
            if self._mpatch_triangle_1:
                self._mpatch_triangle_1.remove()
            
            self._mpatch_triangle_1 = mpatch.Polygon(np.array(self._triangle_1), 2, ec="black", facecolor='#87CEEB')
            self._axis.add_artist(self._mpatch_triangle_1)
            self._triangle_1 = []
    def _draw_triangle_no2(self, x, y):
         # collection of data for drawing triangle
        if self._point_tr_2[2]:
                self._point_tr_2[2] = []
                self._point_tr_2[2].append([x,y])
            
        # number of points
        for i in range(0, 3):
            self._triangle_2.append(self._point_tr_2[i][0])
            
        if len(self._triangle_2) == 3:
            # drawing triangle {robot body}
            if self._mpatch_triangle_2:
                self._mpatch_triangle_2.remove()
            
            self._mpatch_triangle_2 = mpatch.Polygon(np.array(self._triangle_2), 2, ec="black", facecolor='#66FF66')
            self._axis.add_artist(self._mpatch_triangle_2)
            self._triangle_2 = []
    def init_triangles(self):
        self._draw_triangle_no1(340, 100)
        self._draw_triangle_no2(260, 100)
    def loop_draw_object(self, x, y, color, det_obj):
        
        # initialization actual color for drawing
        result_color = self._init_color(color, det_obj)
        # calculation
        for c_idx, col_name in enumerate(self.num_of_c):
            if color == col_name:
                for o_idx in range(0, self.num_of_p[c_idx]):
                    if o_idx == det_obj:
                        # draw objects
                        if color == 'blue':
                            self._draw_objects(x, y, o_idx, c_idx, 15)
                        else:
                            self._draw_objects(x, y, o_idx, c_idx, -107)
                        break
        # draw triangles
        if color == 'blue':
            self._draw_triangle_no1(x, y)
        elif color == 'green':
            self._draw_triangle_no2(x, y)

        # add legend {upper right}
        global rect, tr1, tr2
        tr1 = self._mpatch_triangle_1

        if self._mpatch_triangle_2:
            tr2 = self._mpatch_triangle_2
            self._axis.legend([rect, tr1, tr2], self._labels, loc='upper right', labelspacing= 1, fontsize=8)
    def _cross_vectors(self, triangle):
        PQ = [(triangle[2][0][0] - triangle[0][0][0]), (triangle[2][0][1] - triangle[0][0][1])]
        PR = [(triangle[1][0][0] - triangle[0][0][0]), (triangle[1][0][1] - triangle[0][0][1])]

        PQ_PR_mult    = PQ[0]*PR[0] + PQ[1]*PR[1]
        PQ_PR_multAbs = (math.sqrt(PQ[0]*PQ[0] + PQ[1]*PQ[1]) * math.sqrt(PR[0]*PR[0] + PR[1]*PR[1]))

        return int(math.degrees(math.acos(float(PQ_PR_mult)/float(PQ_PR_multAbs))))
    def calculation_of_robot_output(self):
        # add try exception
        try:
            # calculation angeles {right hand}
            if self._point_tr_2[2][0]:
                self.angle_rh = self._cross_vectors(self._point_tr_2)
            else:
                self.angle_rh = 45
        except ZeroDivisionError:
            self.angle_rh = 45
        # actual robot position {right hand}
        if 45 <= self.angle_rh <= 135:
            self.pos_rh  = int(self.angle_rh*5.56)
        else:
            if self.angle_rh < 45:
                self.pos_rh = 250
            else:
                self.pos_rh = 750
        # calculation angeles {left hand}
        try:
            if self._point_tr_1[2][0]:
                self.angle_lh = self._cross_vectors(self._point_tr_1)
            else:
                self.angle_lh = 45
        except ZeroDivisionError:
            self.angle_lh = 45
        # actual robot position {right hand}
        if 45 <= self.angle_lh <= 135:
            self.pos_lh  = int((180 - self.angle_lh)*5.56)
        else:
            if self.angle_lh < 45:
                self.pos_lh = 750
            else:
                self.pos_lh = 250
    def plot_block_show(self):
        self._plot.show(block=True)
        
        
        
    
