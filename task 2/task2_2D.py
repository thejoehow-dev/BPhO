import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle

N = 150         # number of small particles
L = 20.0        # box size
dt = 0.01       # time step
T = 30.0        # duration
fps = 60

m = 1.0
M = 5.0

r = 0.15
R = 1.0

sigma_v = 5.0       # initial velocity standard deviation

# initial conditions
np.random.seed(42)

# small particles
pos = np.random.uniform(r, L - r, (N, 2))

vel = np.random.normal(0, sigma_v, (N, 2))

# large particle
large_pos = np.array([L/2, L/2], dtype=float)
large_vel = np.array([0.0, 0.0])

# store trajectory
path = [large_pos.copy()]

# figure setup
fig = plt.figure(figsize=(10, 8))
gs = fig.add_gridspec(2,1, height_ratios=[4, 1])

# simulation window
ax = fig.add_subplot(gs[0])
ax.set_xlim(0, L)
ax.set_ylim(0, L)
ax.set_aspect('equal')
ax.set_title("Brownian Motion Simulation")
ax.set_xlabel("x")
ax.set_ylabel("y")

scatter = ax.scatter(pos[:, 0], pos[:, 1], s=10, color="grey")

large_circle = Circle(large_pos, R, color="blue", zorder=1)

ax.add_patch(large_circle)

path_line, = ax.plot([],[], color="black", linewidth=1.5, alpha=0.7)

time_text = ax.text(0.02, 0.98, "", transform=ax.transAxes, va="top")

### trajectory subplot
ax2 = fig.add_subplot(gs[1])

ax2.set_title("Path of Large Particle")
ax2.set_aspect('equal')
ax2.set_xlim(0, L)
ax2.set_ylim(0, L)
ax2.set_xlabel("x")
ax2.set_ylabel("y")

traj_line, = ax2.plot([], [], color="red", linewidth=2)

traj_point, = ax2.plot([],[],"ro")

# physics
def update(frame):
    global pos, vel
    global large_pos, large_vel
    global path

    pos += vel * dt             # move small particles

    # wall collisions
    for d in range(2):
        left = pos[:, d] < r
        right = pos[:, d] > L - r
        vel[left | right, d] *= -1
        pos[:, d] = np.clip(pos[:, d], r, L - r)

    # small-small collisions
    for i in range(N):
        for j in range(i + 1, N):
            delta = pos[j] - pos[i]
            dist = np.linalg.norm(delta)
            min_dist = 2 * r

            if 1e-12 < dist < min_dist:
                n = delta / dist
                rel_vel = vel[i] - vel[j]
                approaching_speed = np.dot(rel_vel, n)
                # skip if separating
                if approaching_speed <= 0:
                    continue

                # equal elastic collision
                impulse = approaching_speed * n
                vel[i] -= impulse
                vel[j] += impulse

                # resolve overlap
                overlap = min_dist - dist
                pos[i] -= 0.5 * overlap * n
                pos[j] += 0.5 * overlap * n

    # move large particle
    large_pos += large_vel * dt
    for d in range(2):
        if large_pos[d] < R:
            large_pos[d] = R
            large_vel[d] *= -1
        elif large_pos[d] > L - R:
            large_pos[d] = L - R
            large_vel[d] *= -1

    # small-large collision
    for i in range(N):
        delta = pos[i] - large_pos
        dist = np.linalg.norm(delta)
        collision_dist = r + R

        if 1e-12 < dist < collision_dist:
            n = delta / dist
            rel_vel = vel[i] - large_vel
            vn = np.dot(rel_vel, n)
            if vn >= 0:
                continue

            # elastic collision
            m1 = m
            m2 = M

            v1 = vel[i]
            v2 = large_vel

            vel[i] = (v1 - (2*m2 / (m1+m2)) * vn * n)

            large_vel = (v2 + (2*m1 / (m1+m2)) * vn * n)

            # remove overlap
            overlap = collision_dist - dist
            pos[i] += overlap * n

    large_vel *= 0.9995             # damping

    # store path
    path.append(large_pos.copy())
    path_arr = np.array(path)

    # update graphics
    scatter.set_offsets(pos)
    large_circle.center = large_pos
    path_line.set_data(path_arr[:, 0], path_arr[:, 1])
    traj_line.set_data(path_arr[:, 0], path_arr[:, 1])
    traj_point.set_data([large_pos[0]], [large_pos[1]])
    time_text.set_text(f"Time = {frame * dt:.2f} s")

    return (scatter, large_circle, path_line, traj_line, traj_point, time_text)

# animation
frames = int(T/dt)
ani = FuncAnimation(fig, update, frames=frames, interval=1000 / fps, blit=False)

plt.tight_layout()
plt.show()
