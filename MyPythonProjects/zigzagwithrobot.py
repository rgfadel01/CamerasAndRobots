import abb
import time

# Connect to the ABB robot
print("Connecting to robot...")
R = abb.Robot(ip='127.0.0.1')  # Replace with actual robot IP if needed
print("Connected.")

# Step 1: Get current joint angles
try:
    joints = R.get_joints()
    print("Current joint angles (deg):", joints)
except Exception as e:
    print("Failed to get joints:", e)
    exit()

# Step 2: Try moving joint 3 slightly (+5 degrees)
try:
    print("Trying to nudge Joint 3 by +5 degrees...")
    new_joints = joints.copy()
    new_joints[2] += 5  # Joint 3 is index 2
    R.move_j(new_joints)
    print("Successfully moved Joint 3.")
except Exception as e:
    print("Error moving Joint 3:", e)
    exit()

# Optional Step 3: Move to a neutral joint configuration
# This avoids being near joint limits for future cartesian moves
try:
    print("Moving to neutral joint pose...")
    neutral_pose = [0, -30, 30, 0, 45, 0]  # example pose; adjust as needed
    R.move_j(neutral_pose)
    print("Moved to neutral pose.")
except Exception as e:
    print("Failed to move to neutral pose:", e)
    exit()

# Final status
print("Robot is now in a safe joint configuration.")
