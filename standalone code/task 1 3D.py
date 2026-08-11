import random
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

N = 50         # steps per walk
W = 5          # number of walks
s = 1          # step size

x = 0
y = 0
z = 0

all_x = []
all_y = []
all_z = []
colours = []

for i in range (W):

    # start where previous walk ended
    x_values = [x]
    y_values = [y]
    z_values = [z]

    colours.append((random.random(),random.random(),random.random()))

    for j in range(0,int(N)):
        theta = random.uniform(0,2*np.pi)
        alpha = random.uniform(0,2*np.pi)
        dx = s*np.sin(theta)*np.cos(alpha)
        dy = s*np.sin(theta)*np.sin(alpha)
        dz = s*np.cos(theta)
        x += dx
        y += dy
        z += dz

        x_values.append(x)
        y_values.append(y)
        z_values.append(z)

    all_x.append(x_values)
    all_y.append(y_values)
    all_z.append(z_values)


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# graph limits
all_x_points = []
all_y_points = []
all_z_points = []

for i in all_x:
    all_x_points.extend(i)

for i in all_y:
    all_y_points.extend(i)

for i in all_z:
    all_z_points.extend(i)

ax.set_xlim(min(all_x_points), max(all_x_points))
ax.set_ylim(min(all_y_points), max(all_y_points))
ax.set_zlim(min(all_z_points), max(all_z_points))
ax.set_box_aspect((max(all_x_points)-min(all_x_points), max(all_y_points)-min(all_y_points), max(all_z_points)-min(all_z_points)))

ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")

plt.get_current_fig_manager().set_window_title("Task 1 - 3D Random Walk")

t1 = "3D Random Walk, "

if N == 1:
    t2 = " step per walk, "
else:
    t2 = " steps per walk, "

if W == 1:
    t3 = " walk, step size "
else:
    t3 = " walks, step size "

ax.set_title(t1 + str(N) + t2 + str(W) + t3 + str(s))

# one line for each walk
lines = []

for colour in colours:
    line, = ax.plot([],[], color=colour, linewidth=1)
    lines.append(line)

# animate

def update(frame):
    for line in lines:
        line.set_data([],[])
        line.set_3d_properties([])
    for i in range(W):
        if frame >= N:
            # entire walk visible
            lines[i].set_data(all_x[i], all_y[i])
            lines[i].set_3d_properties(all_z[i])
        else:
            # only reveal part of walk
            lines[i].set_data(all_x[i][:frame+1], all_y[i][:frame+1])
            lines[i].set_3d_properties(all_z[i][:frame+1])
        frame -= N
        if frame < 0:
            break
    return lines

ani = FuncAnimation(fig, update, frames = W*N + 1, interval = 1, blit = False)

plt.show()
