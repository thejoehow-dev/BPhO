import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

N = 100         # steps per walk
W = 10          # number of walks
s = 1          # step size

x = 0
y = 0

all_x = []
all_y = []
colours = []

for i in range(W):

    # start where previous walk ended
    x_values = [x]
    y_values = [y]

    colours.append((random.random(),random.random(),random.random()))

    for j in range(N):
        theta = random.uniform(0,2*np.pi)
        x += s*np.cos(theta)
        y += s*np.sin(theta)
        x_values.append(x)
        y_values.append(y)

    all_x.append(x_values)
    all_y.append(y_values)

fig, ax = plt.subplots()

# graph limits
all_x_points = []
all_y_points = []

for i in all_x:
    all_x_points.extend(i)

for i in all_y:
    all_y_points.extend(i)

ax.set_xlim(min(all_x_points), max(all_x_points))
ax.set_ylim(min(all_y_points), max(all_y_points))
ax.set_aspect('equal')

ax.set_xlabel("x")
ax.set_ylabel("y")

plt.get_current_fig_manager().set_window_title("Task 1 - 2D Random Walk")

t1 = "2D Random Walk, "

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
    for i in range(W):
        if frame >= N:
            # entire walk visible
            lines[i].set_data(all_x[i], all_y[i])
        else:
            # only reveal part of walk
            lines[i].set_data(all_x[i][:frame + 1], all_y[i][:frame + 1])
        frame -= N
        if frame < 0:
            break
    return lines

ani = FuncAnimation(fig, update, frames = W*N + 1, interval = 1, blit = True)

plt.show()
