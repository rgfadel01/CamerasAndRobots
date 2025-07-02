import time
import math

def run_zigzag_right(R, Total_number_NODES_X, zigzag_width, total_z, step_z=50):
    """
    Scan the right surface in a serpentine (zigzag) pattern:
      - zigzag_width = total Y span to cover (mm)
      - total_z      = total Z span to cover (mm)
      - step_z       = Z step between each row (mm)
      - Total_number_NODES_X is retained for compatibility but not used here.

    The robot’s X (distance from the surface) remains fixed. The tool
    always uses the specified orientation quaternion [0.121, 0.454, -0.543, -0.697].
    """

    def compute_node_1_1(path):
        ys = [pt[0][1] for pt in path]
        zs = [pt[0][2] for pt in path]
        x = path[0][0][0]
        ymid = (min(ys) + max(ys)) / 2
        zmid = (min(zs) + max(zs)) / 2
        ori = path[0][1]
        return [[x, ymid, zmid], ori]

    print(f"Total zones needed in Z: {math.ceil(total_z / step_z)}")

    j = R.get_joints()
    j[0] = 90; j[1] = 0; j[2] = 0
    R.set_joints(j)
    time.sleep(0.5)

    pose0 = R.get_cartesian()
    [x0, y0, z0], _ = pose0

    # Adjust fixed pose center point (tune these offsets if needed)
    x0 = x0  # Depending on camera data # Fixed distance from right wall
    y0 = y0 + 450
    z0 = z0 + 100

    ori = [0.121, 0.454, -0.543, -0.697]

    y_start = y0 - zigzag_width / 2
    z_start = z0 - total_z / 2
    num_steps = int(total_z / step_z)

    path = []
    path.append([[x0, y_start, z_start], ori])
    for i in range(num_steps):
        z_layer = z_start + i * step_z
        z_next = z_layer + step_z
        y_target = y_start + (zigzag_width if i % 2 == 0 else 0)
        path.append([[x0, y_target, z_layer], ori])
        path.append([[x0, y_target, z_next], ori])

    node11 = compute_node_1_1(path)
    print(f"Node 1,1 (mid-point): Pos = {[f'{v:.1f}' for v in node11[0]]}, Ori = {[round(q, 3) for q in node11[1]]}")

    print("\nPlanned target path:")
    for idx, p in enumerate(path, start=1):
        pos, q = p
        print(f"P{idx}: Pos = {[f'{i:.1f}' for i in pos]}, Ori = {[round(o, 3) for o in q]}")

    print("\nMoving to start pose...")
    R.clear_buffer()
    R.buffer_add(path[0])
    R.buffer_execute()
    time.sleep(1)

    print(f"\nExecuting {len(path)} buffered movements...\n")
    R.clear_buffer()
    for p in path:
        R.buffer_add(p)
    R.buffer_execute()

    print(f"\n=== Completed a single right-surface zigzag tile ===")
