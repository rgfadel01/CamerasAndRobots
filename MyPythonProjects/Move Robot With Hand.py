import threading
import cv2
import math
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import abb

# Webcam setup
cap = cv2.VideoCapture(1)
cap.set(3, 1280)
cap.set(4, 720)

# Connect to robot
R = abb.Robot(ip='127.0.0.1')

# Hand detector
detector = HandDetector(detectionCon=0.8, maxHands=1)

# Polyfit for distance calculation
x = [300, 245, 200, 170, 145, 130, 112, 103, 93, 87, 80, 75, 70, 67, 62, 59, 57]
y = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
coff = np.polyfit(x, y, 2)  # y = Ax^2 + Bx + C

# Function to move robot in a thread
def move_robot(distanceCM):
    try:
        # Ensure distanceCM is a single value, not an array
        distance_value = distanceCM[0] if isinstance(distanceCM, np.ndarray) else distanceCM
        R.set_joints([20, 40, 0, 0, 70, 0])
        R.set_external_axis([distance_value, 0, 0, 0, 0, 0])
    except Exception as e:
        print("Error moving robot:", e)

# Loop
while True:
    success, img = cap.read()
    hands, img = detector.findHands(img)

    if hands:
        lmlist = hands[0]['lmList']
        x1, y1, z1 = lmlist[5]
        x2, y2, z2 = lmlist[17]
        distance = (abs(x2 - x1), int(math.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2)))

        A, B, C = coff
        distance_numpy = np.array(distance)
        distanceCM = A * distance_numpy ** 2 + B * distance_numpy + C
        print(distanceCM[0])

        # Launch robot movement in separate thread if needed
        if distanceCM[0] < 60:  # Example trigger condition
            threading.Thread(target=move_robot, args=(distanceCM,)).start()

    cv2.imshow("Image", img)
    cv2.waitKey(1)