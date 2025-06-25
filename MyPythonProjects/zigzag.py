import abb, time, math

def run_zigzag(R, Total_number_NODES_X, zigzag_width, total_z, step_z=50):
    def compute_node_1_1(path):
        xs = [pt[0][0] for pt in path]
        zs = [pt[0][2] for pt in path]
        y = path[0][0][1]
        xmid = (min(xs) + max(xs)) / 2
        zmid = (min(zs) + max(zs)) / 2
        ori = path[0][1]
        return [[xmid, y, zmid], ori]

    print(f"Total zones needed in X: {Total_number_NODES_X}")

    j = R.get_joints()
    j[0] = 90; j[1] = 0; j[2] = 0
    R.set_joints(j)
    time.sleep(0.5)

    pose0 = R.get_cartesian()
    [x0, y0, z0], _ = pose0
    

    ori = [0.8, -0.331, 0.191, 0.462]
    y0= -1800
    z0 =  1400

    x_start = x0 #- zigzag_width / 2
    z_start = z0 - total_z / 2
    num_steps = int(total_z / step_z)

    path = []
    path.append([[x_start, y0, z_start], ori])
    for i in range(num_steps):
        z_layer = z_start + i * step_z
        z_next = z_layer + step_z
        x_target = x_start + (zigzag_width if i % 2 == 0 else 0)
        path.append([[x_target, y0, z_layer], ori])
        path.append([[x_target, y0, z_next], ori])

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

    print(f"\n=== Completed a single zigzag tile ===")
