import cv2
import math
import numpy as np
import abb
import threading

import objectdetection
import json
import os



R = abb.Robot(ip='127.0.0.1')
#R = abb.Robot(ip='192.168.125.1')

R.set_joints([90, 0, 0, 0, 0, 0])  
#R.set_external_axis([4000, 0, 0, 0, 0, 0])
pose = R.get_cartesian()
print("current pose of the robot, in millimeters :",pose)
#
pose0 = R.get_cartesian()
print("Captured orientation:", pose0[1])

external_axes = R.get_external_axis()
print("External axis values:", external_axes)



#ext = R.get_external_axis()
#print("External axes:", ext)