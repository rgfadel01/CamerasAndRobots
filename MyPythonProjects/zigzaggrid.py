import abb, time, math

R = abb.Robot(ip='127.0.0.1')

# parameters
total_area_x = 1500
total_area_z = 1000
tile_w = 500
tile_h = 500
step_z = 50

# 1) zero joints 2&3
j = R.get_joints()
j[1], j[2] = 0, 0
R.set_joints(j)
time.sleep(0.5)

# 2) read home pose & lock orientation
pose0 = R.get_cartesian()
[x0, y0, z0], _ = pose0
ori = [0.8, -0.331, 0.191, 0.462]

# 3) configure a tight zone so point‑motions reconfigure joints smoothly
#    z0 = point‑move zone -> stops briefly and allows joint blend
R.set_zone(zone_key='z0', point_motion=True)

tiles_x = math.ceil(total_area_x / tile_w)
tiles_z = math.ceil(total_area_z / tile_h)
print(f"Tiling {tiles_x}×{tiles_z} of {tile_w}×{tile_h}…")

pt = 1
for ix in range(tiles_x):
    for iz in range(tiles_z):
        ext_x = ix * tile_w
        ext_z = iz * tile_h
        print(f"-- Tile [{ix+1},{iz+1}] ext_axes→ X:{ext_x} Z:{ext_z}")

        # A) move external axes
        R.set_external_axis([ext_x, ext_z, 0,0,0,0])
        time.sleep(0.2)

        # B) immediately give it a safe joint‑space posture
        #    here we simply re‑issue the “home” joint angles we read
        #    that ensures joints stay within limits before Cartesian moves
        R.set_joints([j[0],0,0,j[3],j[4],j[5]])
        time.sleep(0.2)

        # C) move to the corner of this tile in point‑motion
        x_start = x0 - tile_w/2
        z_start = z0 - tile_h/2
        start = [[x_start, y0, z_start], ori]
        print(f"   → start at {[f'{v:.1f}' for v in start[0]]}")
        R.clear_buffer()
        R.buffer_add(start)
        R.buffer_execute()
        time.sleep(0.2)

        # D) build the small zig‑zag within the tile
        layers = int(tile_h/step_z)
        path = []
        for i in range(layers):
            z_l = z_start + i*step_z
            z_n = z_l + step_z
            x_e = x_start + (tile_w if (i%2)==0 else 0)
            path.append([[x_e, y0, z_l], ori])
            path.append([[x_e, y0, z_n], ori])

        # E) log & execute
        for p in path:
            pos, _ = p
            print(f"   P{pt:3d}: {[f'{v:.1f}' for v in pos]}")
            pt += 1

        R.clear_buffer()
        for p in path:
            R.buffer_add(p)
        R.buffer_execute()
        time.sleep(0.2)

print(f"\nDone covering {total_area_x}×{total_area_z} mm.")