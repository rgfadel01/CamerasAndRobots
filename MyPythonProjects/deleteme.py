
import cv2
import math
import numpy as np
import abb
import threading

R = abb.Robot(ip='127.0.0.1')

pose = R.get_cartesian()  # returns ([x, y, z], [q1, q2, q3, q4])
print(pose)