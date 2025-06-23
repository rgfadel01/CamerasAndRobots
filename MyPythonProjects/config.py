import math
import abb
from run_zigzag_top import run_zigzag_top
from zigzag import run_zigzag

from run_zigzag_left import run_zigzag_left
from run_zigzag_right import run_zigzag_right
#R = abb.Robot(ip='127.0.0.1')
R = abb.Robot(ip='192.168.125.1')

# Example parameters:
zigzag_width = 500
total_z = 500
Total_area_X = 500

Total_number_NODES_X = math.ceil(Total_area_X / zigzag_width)
Total_number_NODES_X = max(1, Total_number_NODES_X)

print(f"Will run {Total_number_NODES_X} top‐flange tiles in X")

for i in range(Total_number_NODES_X):
    R.call_flyfrompart()
    #run_zigzag(R, Total_number_NODES_X, zigzag_width, total_z)
    #R.call_flyfrompart()
    #NOT WORKING run_zigzag_left(R, Total_number_NODES_X, zigzag_width, total_z)
    #R.call_flyfrompart()
    #run_zigzag_right(R, Total_number_NODES_X, zigzag_width, total_z)

   # run_zigzag_top(R, Total_number_NODES_X, zigzag_width, total_z)
    #R.call_flyfrompart()

    # shift external axis after each tile, if needed:
   # ext = R.get_external_axis()
   # ext[0] += zigzag_width
   # R.set_external_axis(ext)
   # print(f"Shifted external X by {zigzag_width} mm → now {ext[0]}")

print("All top‐flange tiles done.")



# Example usage (outside this file):
#   from zigzag_top import run_zigzag_top
#
#   R = abb.Robot(ip="127.0.0.1")
#   run_zigzag_top(R, Total_number_NODES_X=3, zigzag_width=500, total_z=500, step_z=50)
