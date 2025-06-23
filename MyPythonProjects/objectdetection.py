import cv2
import numpy as np
import json


#TESTGITHUB
cap = cv2.VideoCapture(1)
cap.set(3, 640)
cap.set(4, 480)
ratio = 0.6961  # cm per pixel
def detect_rectangles(img):
    ratio = 0.6961  # cm per pixel

    # Expected rectangle size in cm
    MIN_WIDTH_CM = 110
    MAX_WIDTH_CM = 125
    MIN_HEIGHT_CM = 90
    MAX_HEIGHT_CM = 105
#KENNY IS WRITING THIS CODE
    rectangles = []

    # Preprocessing
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (7, 7), 0)
    edges = cv2.Canny(blurred, 30, 100)

    # Debug: show preprocessing steps
    cv2.imshow('Gray', gray)
    cv2.imshow('Edges', edges)

    # Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    print(f"Contours found: {len(contours)}")

    debug_img = img.copy()
    cv2.drawContours(debug_img, contours, -1, (0,0,255), 2)
    cv2.imshow('All Contours', debug_img)

    for cnt in contours:
        area = cv2.contourArea(cnt)
        rect = cv2.minAreaRect(cnt)
        width_px, height_px = rect[1]
        if width_px == 0 or height_px == 0:
            continue

        width_cm = width_px * ratio
        height_cm = height_px * ratio
        w_cm, h_cm = max(width_cm, height_cm), min(width_cm, height_cm)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        center = np.mean(box, axis=0).astype(int)

        if (MIN_WIDTH_CM < w_cm < MAX_WIDTH_CM) and (MIN_HEIGHT_CM < h_cm < MAX_HEIGHT_CM):
            print(f"DETECTED: width_cm={w_cm:.1f}, height_cm={h_cm:.1f}")
            cv2.drawContours(img, [box], 0, (0,255,0), 3)
            cv2.putText(img, f"{w_cm:.1f}x{h_cm:.1f}cm", tuple(box[0]),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)
            cv2.circle(img, tuple(center), 5, (255,0,0), -1)
            cv2.imshow("Detected Rectangles", img)
            print("Is this the rectangle you want? (y/n, ESC to exit)")
            key = cv2.waitKey(0)
            if key == ord('y'):
                print("Rectangle confirmed by user.")
                rectangles.append((box, w_cm, h_cm, rect[2], center, rect, area))
                break
            elif key == 27:  # ESC
                print("Exiting.")
                exit()
            else:
                print("Continuing to next detection.")

    return rectangles

# To avoid asking about the same rectangle again
asked_rects = []

def rect_signature(rect):
    # Use center, width, height, angle rounded to 1 decimal as a signature
    center, size, angle = rect[5]
    return (        round(center[0]/2)*2,
        round(center[1]/2)*2,
        round(size[0]/2)*2,
        round(size[1]/2)*2,
        round(angle/2)*2)

while True:
    success, img = cap.read()
    if not success:
        break

    rectangles = detect_rectangles(img)
    found_new = False

    for idx, (box, width_cm, height_cm, angle, center, rect, area) in enumerate(rectangles, 1):
       # sig = rect_signature((box, width_cm, height_cm, angle, center, rect, area))
        sig = rect_signature((box, width_cm, height_cm, rect[2], center, rect, area))

        if sig in asked_rects:
            continue  # Already asked about this rectangle
        found_new = True
        cv2.drawContours(img, [box], 0, (0, 255, 0), 2)
        cv2.putText(img, f"{idx}", tuple(center), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
        cv2.putText(img, f"Rect {idx}: {width_cm:.1f}cm x {height_cm:.1f}cm angle={angle:.1f}",
                    (box[0][0], box[0][1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        # --- NEW: Distance from left edge to rectangle's leftmost point ---
        leftmost_x = np.min(box[:, 0])
        dist_from_left_cm = leftmost_x * ratio
        cv2.putText(img, f"Dist from left: {dist_from_left_cm:.1f}cm", (leftmost_x, center[1]+40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2)
        print(f"Dist from left edge: {dist_from_left_cm:.1f}cm")

        cv2.imshow('Rectangle Detection', img)
        print("Is this the object you are looking for? (y/n) (Press window to focus, then type in terminal)")
        key = cv2.waitKey(0)
        
        
        
        if key in [ord('y'), ord('Y')]:
            print(f"Rotated Rect: center=({rect[0][0]:.1f},{rect[0][1]:.1f}), w={rect[1][0]:.1f}, h={rect[1][1]:.1f}, "
                  f"width_cm={width_cm:.1f}, height_cm={height_cm:.1f}, angle={angle:.1f}, area={area:.0f}, "
                  f"dist_from_left={dist_from_left_cm:.1f}cm")
            rect_data = {
                "center": [float(rect[0][0]), float(rect[0][1])],
                "width_px": float(rect[1][0]),
                "height_px": float(rect[1][1]),
                "width_cm": float(width_cm),
                "height_cm": float(height_cm),
                "angle": float(angle),
                "area": float(area),
                "dist_from_left_cm": float(dist_from_left_cm),
                "box": box.tolist()
            }
            with open("detected_rectangle.json", "w") as f:
                json.dump(rect_data, f, indent=2)
            print("Saved rectangle data to detected_rectangle.json")
            cap.release()
            cv2.destroyAllWindows()
            exit(0)
        else:
            asked_rects.append(sig)
            print("Okay, searching for another rectangle...")

    if not found_new:
        cv2.imshow('Rectangle Detection', img)
        if cv2.waitKey(1) == 27:  # ESC to exit
            break

cap.release()
cv2.destroyAllWindows()



if key in [ord('y'), ord('Y')]:
    rect_data = {
        "center": [float(rect[0][0]), float(rect[0][1])],
        "width_px": float(rect[1][0]),
        "height_px": float(rect[1][1]),
        "width_cm": float(width_cm),
        "height_cm": float(height_cm),
        "angle": float(angle),
        "area": float(area),
        "dist_from_left_cm": float(dist_from_left_cm),
        "box": box.tolist()
    }
    with open("detected_rectangle.json", "w") as f:
        json.dump(rect_data, f, indent=2)
    print("Saved rectangle data to detected_rectangle.json")
    cap.release()
    cv2.destroyAllWindows()
    exit(0)