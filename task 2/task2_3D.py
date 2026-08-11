import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D

N = 150         # number of small particles
L = 20.0        # box size
dt = 0.01       # time step
T = 20.0        # duration
fps = 60

m = 1.0
M = 5.0

r = 0.15
R = 1.0

sigma_v = 5.0       # initial velocity standard deviation

# initial conditions

np.random.seed(42)

pos = np.random.uniform(r, L-r, (N,3))
vel = np.random.normal(0, sigma_v, (N,3))
large_pos = np.array([L/2,L/2,L/2], dtype=float)
large_vel = np.zeros(3)
path = [large_pos.copy()]

# figure

fig = plt.figure(figsize=(10,8))
ax = fig.add_subplot(111, projection='3d')

ax.set_xlim(0,L)
ax.set_ylim(0,L)
ax.set_zlim(0,L)

ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")

ax.set_title("3D Brownian Motion Simulation")
plt.get_current_fig_manager().set_window_title("Task 2 - 3D Brownian Motion Simulation")

# small particles
scatter = ax.scatter(pos[:,0], pos[:,1], pos[:,2], s=5)

# large particle
large_scatter = ax.scatter([large_pos[0]], [large_pos[1]], [large_pos[2]], s=500, c='blue')

# trajectory

path_line, = ax.plot([], [], [], 'k-', linewidth=2)

time_text = ax.text2D(0.02, 0.95, "", transform=ax.transAxes)

# update function

def update(frame):
    global pos, vel, large_pos, large_vel, path

    # move small particles
    pos += vel * dt

    # wall collisions
    for d in range(3):
        low = pos[:,d] < r
        high = pos[:,d] > L-r
        vel[low | high,d] *= -1
        pos[:,d] = np.clip(pos[:,d], r, L-r)

    # small-small collisions
    for i in range(N):
        for j in range(i+1,N):
            delta = pos[j] - pos[i]
            dist = np.linalg.norm(delta)
            min_dist = 2*r

            if 1e-12 < dist < min_dist:
                n = delta/dist
                rel_vel = vel[i] - vel[j]
                vn = np.dot(rel_vel,n)
                if vn <= 0:
                    continue

                impulse = vn*n
                vel[i] -= impulse
                vel[j] += impulse
                overlap = min_dist-dist
                pos[i] -= 0.5*overlap*n
                pos[j] += 0.5*overlap*n

    # move large particle
    large_pos += large_vel*dt
    for d in range(3):

        if large_pos[d] < R:
            large_pos[d] = R
            large_vel[d] *= -1

        elif large_pos[d] > L-R:
            large_pos[d] = L-R
            large_vel[d] *= -1

    # small-large collision
    for i in range(N):
        delta = pos[i] - large_pos
        dist = np.linalg.norm(delta)

        collision_dist = (r + R)

        if 1e-12 < dist < collision_dist:
            n = delta/dist
            rel_vel = (vel[i] - large_vel)

            vn = np.dot(rel_vel,n)
            if vn >= 0:
                continue

            m1 = m
            m2 = M
            v1 = vel[i]
            v2 = large_vel

            vel[i] = (v1 - (2*m2/(m1+m2)) * vn * n)
            large_vel = (v2 + (2*m1/(m1+m2)) * vn * n)
            overlap = (collision_dist-dist)
            pos[i] += overlap*n

    large_vel *= 0.9995         # damping

    # store path
    path.append(large_pos.copy())
    path_arr = np.array(path)

    # update graphics
    scatter._offsets3d = (pos[:,0], pos[:,1], pos[:,2])
    large_scatter._offsets3d = ([large_pos[0]], [large_pos[1]], [large_pos[2]])
    path_line.set_data(path_arr[:,0], path_arr[:,1])
    path_line.set_3d_properties(path_arr[:,2])
    time_text.set_text(f"Time = {frame*dt:.2f} s")

    return (scatter, large_scatter, path_line, time_text)

# animation

frames = int(T/dt)
ani = FuncAnimation(fig, update, frames=frames, interval=1000/fps, blit=False)

plt.show()
