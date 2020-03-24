'''
Created on Jan 15, 2017

@author: roman_parak
'''

import cv2
import sys
import numpy as np
import math
import object_draw_bioloid


def main(argv=sys.argv):
	# number of individual colors for input -> ['blue', 'green']
	b_tObj = object_draw_bioloid.tracking_bioloid(1,1)
	# set maximum limits {x, y} of frame
	b_tObj.axis_init(640, 480)
	# initialization triangles
	b_tObj.init_triangles()

	b_tObj.loop_draw_object(100, 250, 'green', 0)
	b_tObj.loop_draw_object(100, 250, 'green', 0)
	b_tObj.loop_draw_object(500, 120, 'blue', 0)
	b_tObj.loop_draw_object(500, 120, 'blue', 0)


if __name__ == "__main__":
	sys.exit(main())
