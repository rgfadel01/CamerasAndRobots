import cv2
import math
import numpy as np

points = []
ratio = 10 / 114  # Pixels to cm conversion ratio
measurement_array = np.zeros((1, 5))  # 1 row, 5 columns

def draw_circle(event, x, y, flags, params):
    global points
    if event == cv2.EVENT_LBUTTONDOWN and len(points) < 6:
        points.append((x, y))

cv2.namedWindow("Frame")
cv2.setMouseCallback("Frame", draw_circle)

cap = cv2.VideoCapture(1)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to read from camera.")
        break

    for pt in points:
        cv2.circle(frame, pt, 5, (0, 0, 255), -1)

    for i in range(0, len(points) - 1, 2):
        if i // 2 < 3:
            pt1, pt2 = points[i], points[i + 1]
            distance_px = math.hypot(pt2[0] - pt1[0], pt2[1] - pt1[1])
            distance_cm = round(ratio * distance_px, 2)

            cv2.putText(frame, f"{distance_cm} cm", (pt1[0], pt1[1] - 10),
                        cv2.FONT_HERSHEY_PLAIN, 2.5, (25, 15, 235), 2)

            if measurement_array[0, i // 2] == 0:
                measurement_array[0, i // 2] = distance_cm
                print("Measurement array:")
                print(measurement_array)

    # Auto-reset after 6 points (3 measurements)
    if len(points) == 6:
        print("Finished 3 measurements. Resetting...")
        points = []
        measurement_array = np.zeros((1, 5))

    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) == 27:  # ESC to exit
        break

cap.release()
cv2.destroyAllWindows()