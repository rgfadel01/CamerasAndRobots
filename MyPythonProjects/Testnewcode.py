import cv2
import math
import numpy as np
import abb
import threading

import cv2
import math
import numpy as np

#ratio = 0.6961  # cm per pixel
#points = []

#def mouse_callback(event, x, y, flags, param):
 #   global points
  #  if event == cv2.EVENT_LBUTTONDOWN and len(points) < 4:
   #     points.append((x, y))

#cv2.namedWindow("Test Rectangle")
#cv2.setMouseCallback("Test Rectangle", mouse_callback)
#cap = cv2.VideoCapture(1)  # Change index if needed

#while True:
 #   ret, frame = cap.read()
  #  if not ret:
   #     print("Camera not found.")
    #    break

    #display = frame.copy()
    #for pt in points:
     #   cv2.circle(display, pt, 5, (0, 0, 255), -1)

  #  if len(points) == 4:
   #     pts = np.array(points, dtype=np.int32)
    #    cv2.polylines(display, [pts], isClosed=True, color=(0,255,0), thickness=2)

        # Order points: top-left, top-right, bottom-right, bottom-left
     #   rect = cv2.boundingRect(pts)
      #  x, y, w, h = rect
       # roi_corners = pts[np.argsort(pts[:,1])]  # sort by y
        #top_pts = roi_corners[:2][np.argsort(roi_corners[:2,0])]  # sort top two by x
        #bottom_pts = roi_corners[2:][np.argsort(roi_corners[2:,0])]  # sort bottom two by x
        #ordered = np.array([top_pts[0], top_pts[1], bottom_pts[1], bottom_pts[0]])

        # Compute width and height in pixels
   #     width_px = math.hypot(ordered[1][0] - ordered[0][0], ordered[1][1] - ordered[0][1])
    #    height_px = math.hypot(ordered[0][0] - ordered[3][0], ordered[0][1] - ordered[3][1])
     #   width_cm = width_px * ratio
      #  height_cm = height_px * ratio

       # cv2.putText(display, f"W: {width_px:.1f}px / {width_cm:.1f}cm", 
        #            (ordered[0][0], ordered[0][1] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)
        #cv2.putText(display, f"H: {height_px:.1f}px / {height_cm:.1f}cm", 
         #           (ordered[0][0], ordered[0][1] - 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)
     # Calculate and display rectangle center
#        center_x = sum([p[0] for p in points]) / 4
 #       center_y = sum([p[1] for p in points]) / 4
  #      frame_h, frame_w = frame.shape[:2]
   #     cv2.circle(display, (int(center_x), int(center_y)), 8, (255, 0, 255), -1)
    #    cv2.putText(display, f"Center ({int(center_x)}, {int(center_y)})", 
     #               (int(center_x)+10, int(center_y)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,0,255), 2)
      #  print(f"Rectangle center: ({center_x:.1f}, {center_y:.1f})")
       # print(f"Image center: ({frame_w/2:.1f}, {frame_h/2:.1f})")
#    cv2.imshow("Test Rectangle", display)
 #   key = cv2.waitKey(1)
  #  if key == 27:  # ESC to exit
   #     break
   # if key == ord('r'):
    #    points = []

#cap.release()
#cv2.destroyAllWindows()


#ratio = 0.6961  # cm per pixel
#points = []

#def mouse_callback(event, x, y, flags, param):
 #   global points
 #   if event == cv2.EVENT_LBUTTONDOWN and len(points) < 2:
  #      points.append((x, y))

#cv2.namedWindow("Test")
#cv2.setMouseCallback("Test", mouse_callback)
#cap = cv2.VideoCapture(1)  # Change index if needed

#while True:
 #   ret, frame = cap.read()
  #  if not ret:
   #     print("Camera not found.")
    #    break

    #for pt in points:
     #   cv2.circle(frame, pt, 5, (0, 0, 255), -1)

   # if len(points) == 2:
    #    p1, p2 = points
     #   d_px = math.hypot(p2[0] - p1[0], p2[1] - p1[1])
      #  d_cm = d_px * ratio
       # cv2.line(frame, p1, p2, (0, 255, 0), 2)
        #cv2.putText(frame, f"{d_cm:.2f} cm", (p1[0], p1[1] - 10),
                  #  cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # cv2.imshow("Test", frame)
    # key = cv2.waitKey(1)
    # if key == 27:  # ESC to exit
    #     break
    # if key == ord('r'):
    #     points = []

# cap.release()
#  cv2.destroyAllWindows()





# --- Robot Initialization ---
R = abb.Robot(ip='127.0.0.1')
#R = abb.Robot(ip='192.168.125.1')
#R.call_flyfrompart()


R.set_joints([90, 0, 0, 0, 0, 0])  

pose = R.get_cartesian()
print("current pose of the robot, in millimeters :",pose)

pose0 = R.get_cartesian()
print("Captured orientation:", pose0[1])


# To turn doMaterialOn HIGH:
#R.set_dio(True)
#cv2.waitKey(5000)
#R.set_dio(False)
#R.set_external_axis([4000.0, 0.0, 0.0, 0.0, 89999994.0, 89999994.0])
#R.set_joints([0, 0, 0, 0, 0, 0])


external_axes = R.get_external_axis()
print("External axis values:", external_axes)



#ext = R.get_external_axis()
#print("External axes:", ext)


# 1) Query the current external‑axis values
#ext = R.get_external_axis()    # returns a list of six numbers [a, b, c, d, e, f]
#print("Before shift, external axes:", ext)

# 2) Modify axis 1 (the first element in that list) by +500 mm
#ext[0] += 500.0

# 3) Send the updated external‑axis command back to the robot
#R.set_external_axis(ext)
#print("After shift, external axes:", ext)