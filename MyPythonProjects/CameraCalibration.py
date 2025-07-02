
import cv2
import math
import numpy as np
import abb
import threading
import objectdetection
import json
import os


#ratio = 0.6961  # cm per pixel
ratio = 0.755  # cm per pixel
#new_ratio = 0.6961 * (100 / 97) ≈ 0.7176
points = []

def mouse_callback(event, x, y, flags, param):
    global points
    if event == cv2.EVENT_LBUTTONDOWN and len(points) < 2:
        points.append((x, y))

cv2.namedWindow("Test")
cv2.setMouseCallback("Test", mouse_callback)
cap = cv2.VideoCapture(1)  # Change index if needed

while True:
    ret, frame = cap.read()
    if not ret:
        print("Camera not found.")
        break

    for pt in points:
        cv2.circle(frame, pt, 5, (0, 0, 255), -1)

    if len(points) == 2:
        p1, p2 = points
        d_px = math.hypot(p2[0] - p1[0], p2[1] - p1[1])
        d_cm = d_px * ratio
        cv2.line(frame, p1, p2, (0, 255, 0), 2)
        cv2.putText(frame, f"{d_cm:.2f} cm", (p1[0], p1[1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Test", frame)
    key = cv2.waitKey(1)
    if key == 27:  # ESC to exit
        break
    if key == ord('r'):
        points = []
cap.release()
cv2.destroyAllWindows()