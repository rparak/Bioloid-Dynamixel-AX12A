#########################################################################################################
# ============================== BRNO UNIVERSITY OF TECHNOLOGY ======================================== #
# ============================== FACULTY OF MECHANICAL ENGINEERING ==================================== #
# =========================INSITUTE OF AUTOMATION AND COMPUTER SCIENCE ================================ #
# Autor: Roman Parak
#########################################################################################################

import sys
import object_draw_bioloid
import time
import math
import numpy as np

def main(argv=sys.argv):
	# number of individual colors for input -> ['blue', 'green']
	b_tObj = object_draw_bioloid.tracking_bioloid(1,1)
	# set maximum limits {x, y} of frame
	b_tObj.axis_init(640, 480)
	# initialization triangles

	b_tObj.control_rect(350, 100)       

	#print(b_tObj.pos_rh, b_tObj.pos_lh)
	b_tObj.plot_block_show()
if __name__ == "__main__":
    sys.exit(main())
