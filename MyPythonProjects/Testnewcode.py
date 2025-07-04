import cv2
import math
import numpy as np
import abb
import threading
import objectdetection
import json
import os
import time


from run_zigzag_top import run_zigzag_top
from zigzag import run_zigzag
from run_zigzag_left import run_zigzag_left
from run_zigzag_right import run_zigzag_right


R = abb.Robot(ip='127.0.0.1')
#R = abb.Robot(ip='192.168.125.1')

#R.set_joints([90, 0, 0, 0, 0, 0])  
#time.sleep(2)
#R.set_external_axis([4000, 0, 0, 0, 0, 0])
#pose = R.get_cartesian()
#print("current pose of the robot, in millimeters :",pose)
#

#pose0 = R.get_cartesian()
#print("Captured orientation:", pose0[1])

#external_axes = R.get_external_axis()
#print("External axis values:", external_axes)


# Example parameters:
zigzag_width = 1150
total_z = 700
Total_area_X = 700



#zigzag_width = 750
#total_z = 500
#Total_area_X = 500

Total_number_NODES_X = math.ceil(Total_area_X / zigzag_width)
Total_number_NODES_X = max(1, Total_number_NODES_X)


for i in range(Total_number_NODES_X):
    R.call_flyfrompart()
    #time.sleep(0.1)
    run_zigzag(R, Total_number_NODES_X, zigzag_width, total_z)
    #R.call_flyfrompart()
   # run_zigzag_top(R, Total_number_NODES_X, zigzag_width, total_z)
    R.call_flyfrompart()
    


#ext = R.get_external_axis()
#print("External axes:", ext)