import time
import math

def run_zigzag_left(R, Total_number_NODES_Y, zigzag_width, total_z, step_z=50):
    """
    Scan the left surface (vertical YZ plane) in a serpentine (zigzag) pattern:
      - zigzag_width = total Y span to cover (mm)
      - total_z      = total Z span to cover (mm)
      - step_z       = Z step between each row (mm)
      - Total_number_NODES_Y = number of Y nodes per row

    The robot’s X remains at its current value (constant). The tool
    always uses the captured orientation quaternion [0.892, -0.099, 0.37, -0.239].
    """

    def compute_node_1_1(path):
        ys = [pt[0][1] for pt in path]
        zs = [pt[0][2] for pt in path]
        x  = path[0][0][0]
        ymid = (min(ys) + max(ys)) / 2
        zmid = (min(zs) + max(zs)) / 2
        ori  = path[0][1]
        return [[x, ymid, zmid], ori]

    print(f"Total serpentine rows in Z: {math.ceil(total_z / step_z)}, "
          f"Y span = {zigzag_width} mm, Z span = {total_z} mm, step = {step_z} mm")

    # 1) Reset J1–J3 for a safe upright stance
    j = R.get_joints()
    j[0], j[1], j[2] = 90, 0, 0
    R.set_joints(j)
    time.sleep(0.5)

    # 2) Read current Cartesian position (we'll keep X constant)
    pose0 = R.get_cartesian()
    [x0, y0, z0], _ = pose0
    x0 = x0 + 0      # X is constant for left surface
    y0 = y0          # adjust as needed
    z0 = z0 + 0      # adjust as needed

    # 3) Use the captured orientation for the spray gun
    ori_left = [0.892, -0.099, 0.37, -0.239]

    # 4) Compute the YZ extents (centered on current (y0, z0))
    half_y = zigzag_width / 2
    half_z = total_z / 2

    y_start = y0 - half_y
    y_end   = y0 + half_y
    z_start = z0 - half_z

    num_rows = int(math.ceil(total_z / step_z))

    # 5) Build the serpentine path in the YZ plane:
    #    - On even rows, go Y_start→Y_end
    #    - On odd  rows, go Y_end  →Y_start
    #    - At the end of each row, step Z by step_z (except after the last row)
    path = []
    for row in range(num_rows):
        z_row = z_start + row * step_z
        if row % 2 == 0:
            # bottom→top
            path.append([[x0, y_start, z_row], ori_left])
            path.append([[x0, y_end,   z_row], ori_left])
        else:
            # top→bottom
            path.append([[x0, y_end,   z_row], ori_left])
            path.append([[x0, y_start, z_row], ori_left])

        # If not the very last row, add the vertical step in Z (stay at current Y)
        if row < num_rows - 1:
            next_z = z_start + (row + 1) * step_z
            if row % 2 == 0:
                # we ended at (x0, y_end, z_row), so go to (x0, y_end, next_z)
                path.append([[x0, y_end, next_z], ori_left])
            else:
                # we ended at (x0, y_start, z_row), so go to (x0, y_start, next_z)
                path.append([[x0, y_start, next_z], ori_left])

    # 6) Debug: show “node 1,1” (midpoint of the covered area) and entire path
    node11 = compute_node_1_1(path)
    print(f"Node 1,1 (mid-point of YZ): Pos = {[f'{v:.1f}' for v in node11[0]]}, "
          f"Ori = {[round(q, 3) for q in node11[1]]}")

    print("\nPlanned left-surface serpentine path:")
    for idx, (pos, quat) in enumerate(path, start=1):
        print(f"P{idx}: Pos = {[f'{v:.1f}' for v in pos]}, Ori = {[round(o, 3) for o in quat]}")

    # 7) Move to first waypoint, then execute full buffered path
    print("\nMoving to start pose (left surface serpentine)...")
    R.clear_buffer()
    R.buffer_add(path[0])
    R.buffer_execute()
    time.sleep(1)

    print(f"\nExecuting {len(path)} buffered movements...\n")
    R.clear_buffer()
    for p in path:
        R.buffer_add(p)
    R.buffer_execute()

    print(f"\n=== Completed a single left-surface serpentine tile ===")