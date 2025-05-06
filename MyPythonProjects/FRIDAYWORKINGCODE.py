import cv2
import math
import numpy as np
import abb
import threading

# --- Robot Initialization ---
R = abb.Robot(ip='127.0.0.1')

# --- Measurement and Control Variables ---
points = []                                # clicked points
ratio = 10 / 114                           # pixel-to-cm conversion
measurement_array = np.zeros((1, 5))       # storage for 5 measurements
robot_moved = False                        # flag: robot has been moved after 5 measurements

# --- Functions ---

def move_robot_after_measurements(measurements):
    """
    Compute external axis values from the first two measurements
    and send the joint + external axis commands to the robot.
    """
    try:
        # Axis 1 logic (based on first measurement)
        m1 = measurements[0]
        value1 = 1000 if m1 > 10 else 0

        # Axis 2 logic (based on second measurement)
        m2 = measurements[1]
        if m2 < 10:
            value2 = 0
        elif m2 <= 20:
            value2 = 500
        else:
            value2 = 1000

        # Send commands to robot
        R.set_joints([20, 40, 0, 0, 70, 0])  
        R.set_external_axis([value1, value2, 0, 0, 0, 0])
        print(f"Moved robot → ext axes: [{value1}, {value2}, 0, 0, 0, 0]")
    except Exception as e:
        print("Error moving robot:", e)

def draw_circle(event, x, y, flags, params):
    """
    Mouse callback: collect up to 10 click points.
    """
    global points
    if event == cv2.EVENT_LBUTTONDOWN and len(points) < 10:
        points.append((x, y))

# --- Setup OpenCV window and callback ---
cv2.namedWindow("Frame")
cv2.setMouseCallback("Frame", draw_circle)
cap = cv2.VideoCapture(1)  # try index 0 (adjust if needed)

# --- Main Loop ---
while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to read from camera.")
        break

    # Draw clicked points
    for pt in points:
        cv2.circle(frame, pt, 5, (0, 0, 255), -1)

    # For each pair of points, compute and display distance and store measurement
    for i in range(0, len(points) - 1, 2):
        pair_index = i // 2
        if pair_index < 5:
            p1, p2 = points[i], points[i+1]
            d_px = math.hypot(p2[0] - p1[0], p2[1] - p1[1])
            d_cm = round(ratio * d_px, 2)

            # Display on frame
            cv2.putText(frame, f"{d_cm} cm", (p1[0], p1[1] - 10),
                        cv2.FONT_HERSHEY_PLAIN, 2.5, (25, 15, 235), 2)

            # Store measurement once
            if measurement_array[0, pair_index] == 0:
                measurement_array[0, pair_index] = d_cm
                print("Measurement array:", measurement_array)

    # Once we have 10 clicks (5 measurements), move robot then reset
    if len(points) == 10 and not robot_moved:
        print("All 5 measurements complete.")
        print("Final measurement array:", measurement_array)
        # Move robot in a separate thread to avoid blocking UI
        threading.Thread(target=move_robot_after_measurements, args=(measurement_array[0],)).start()
        robot_moved = True

    # After movement, reset for next cycle
    if len(points) == 10 and robot_moved:
        # small delay to allow user to see final frame
        cv2.waitKey(500)
        points = []
        measurement_array = np.zeros((1, 5))
        robot_moved = False
        print("Resetting for next set of measurements.")

    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) == 27:  # ESC to exit
        break

cap.release()
cv2.destroyAllWindows()
