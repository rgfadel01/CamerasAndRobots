import abb, time, math

def run_zigzag_top(R, Total_number_NODES_X, zigzag_width, total_z, step_z=50):
    """
    Scan the top flange (flat XY plane) in a serpentine (zigzag) pattern:
      - zigzag_width = total X span to cover (mm)
      - total_z      = total Y span to cover (mm)
      - step_z       = Y step between each row (mm)
      - Total_number_NODES_X is retained for compatibility but not used here.

    The robot’s Z (height) remains at its current value (flat surface). The tool
    always uses the “gun-down” orientation quaternion [0.331, -0.8, 0.462, 0.191].
    """

    # Helper: compute the midpoint of the XY area (for debug)
    def compute_node_1_1(path):
        xs = [pt[0][0] for pt in path]
        ys = [pt[0][1] for pt in path]
        z  = path[0][0][2]
        xmid = (min(xs) + max(xs)) / 2
        ymid = (min(ys) + max(ys)) / 2
        ori  = path[0][1]
        return [[xmid, ymid, z], ori]

    print(f"Total serpentine rows in Y: {math.ceil(total_z / step_z)}, "
          f"X span = {zigzag_width} mm, Y span = {total_z} mm, step = {step_z} mm")

    # 1) Reset J1–J3 for a safe upright stance
    j = R.get_joints()
    j[0], j[1], j[2] = 90, 0, 0
    R.set_joints(j)
    time.sleep(0.5)

    # 2) Read current Cartesian position (we'll keep Z constant)
    pose0 = R.get_cartesian()
    [x0, y0, z0], _ = pose0
    y0=y0+450
    z0=z0+100

    # 3) Use the jogged‐down quaternion for the spray gun
    ori_top = [0.331, -0.8, 0.462, 0.191]

    # 4) Compute the XY extents (centered on current (x0,y0))
    half_x = zigzag_width / 2
    half_y = total_z / 2

    x_start = x0 - half_x
    x_end   = x0 + half_x
    y_start = y0 - half_y
    # We'll step from y_start up in increments of step_z

    num_rows = int(math.ceil(total_z / step_z))

    # 5) Build the serpentine path in the XY plane:
    #    - On even rows, go X_start→X_end
    #    - On odd  rows, go X_end  →X_start
    #    - At the end of each row, step Y by step_z (except after the last row)
    path = []
    for row in range(num_rows):
        y_row = y_start + row * step_z
        if row % 2 == 0:
            # left→right
            path.append([[x_start, y_row, z0], ori_top])
            path.append([[x_end,   y_row, z0], ori_top])
        else:
            # right→left
            path.append([[x_end,   y_row, z0], ori_top])
            path.append([[x_start, y_row, z0], ori_top])

        # If not the very last row, add the vertical step in Y (stay at current X)
        if row < num_rows - 1:
            next_y = y_start + (row + 1) * step_z
            # After moving horizontally, move straight “up” in Y:
            if row % 2 == 0:
                # we ended at (x_end, y_row), so go to (x_end, next_y)
                path.append([[x_end, next_y, z0], ori_top])
            else:
                # we ended at (x_start, y_row), so go to (x_start, next_y)
                path.append([[x_start, next_y, z0], ori_top])

    # 6) Debug: show “node 1,1” (midpoint of the covered area) and entire path
    node11 = compute_node_1_1(path)
    print(f"Node 1,1 (mid-point of XY): Pos = {[f'{v:.1f}' for v in node11[0]]}, "
          f"Ori = {[round(q, 3) for q in node11[1]]}")

    print("\nPlanned top‐flange serpentine path:")
    for idx, (pos, quat) in enumerate(path, start=1):
        print(f"P{idx}: Pos = {[f'{v:.1f}' for v in pos]}, Ori = {[round(o, 3) for o in quat]}")

    # 7) Move to first waypoint, then execute full buffered path
    print("\nMoving to start pose (top flange serpentine)...")
    R.clear_buffer()
    R.buffer_add(path[0])
    R.buffer_execute()
    time.sleep(1)

    print(f"\nExecuting {len(path)} buffered movements...\n")
    R.clear_buffer()
    for p in path:
        R.buffer_add(p)
    R.buffer_execute()

    print(f"\n=== Completed a single top‐flange serpentine tile ===")
    