import math
import customtkinter as ctk
import tkinter as tk

root = ctk.CTk()
root.title("Mismatch Probabilities")
root.geometry("700x800")

# variables
canvas_size = 600
radius = 220
cx = canvas_size // 2
cy = canvas_size // 2

angle1 = 30
angle2 = 330

dragging = None

canvas = tk.Canvas(root, width=canvas_size, height=canvas_size, bg="#242424", highlightthickness=0)
canvas.pack(pady=10)

angle_frame = ctk.CTkFrame(root, fg_color="transparent")
angle_frame.pack(pady=10)

angle1_label = ctk.CTkLabel(angle_frame, text="", font=("Arial", 20), text_color="cyan")
angle1_label.pack(side="left", padx=(0,20))

angle2_label = ctk.CTkLabel(angle_frame, text="", font=("Arial", 20), text_color="magenta")
angle2_label.pack(side="left")

classical_label = ctk.CTkLabel(root, text="", font=("Arial", 20))
classical_label.pack(pady=5)

quantum_label = ctk.CTkLabel(root, text="", font=("Arial", 20))
quantum_label.pack(pady=5)

def angle_to_xy(angle):
    radians = math.radians(angle-90)
    x = cx + radius*math.cos(radians)
    y = cy + radius*math.sin(radians)
    return x, y

def xy_to_angle(x, y):
    dx = x - cx
    dy = y - cy
    angle = math.degrees(math.atan2(dy,dx))
    angle = (angle + 90) % 360
    return angle

def draw():
    global handle1, handle2
    canvas.delete("all")

    # vertical dotted line
    canvas.create_line(cx, cy, cx, cy-radius, fill="white", dash=(4,6), width=2)

    # marker positions
    x1, y1 = angle_to_xy(angle1)
    x2, y2 = angle_to_xy(angle2)

    # angle lines
    canvas.create_line(cx, cy, x1, y1, fill="cyan", width=3)
    canvas.create_line(cx, cy, x2, y2, fill="magenta", width=3)

    # arrow heads
    mag = 12
    handle1 = canvas.create_polygon(
        x1 + mag*math.sin(math.radians(angle1)),
        y1 - mag*math.cos(math.radians(angle1)),
        x1 + mag*math.cos(math.radians(angle1)),
        y1 + mag*math.sin(math.radians(angle1)),
        x1 - mag*math.cos(math.radians(angle1)),
        y1 - mag*math.sin(math.radians(angle1)),
        fill="cyan", width=3)

    handle2 = canvas.create_polygon(
        x2 + mag*math.sin(math.radians(angle2)),
        y2 - mag*math.cos(math.radians(angle2)),
        x2 + mag*math.cos(math.radians(angle2)),
        y2 + mag*math.sin(math.radians(angle2)),
        x2 - mag*math.cos(math.radians(angle2)),
        y2 - mag*math.sin(math.radians(angle2)),
        fill="magenta", width=3)

    angle1_label.configure(text=f"Angle 1: {angle1:.1f}°")
    angle2_label.configure(text=f"Angle 2: {angle2:.1f}°")

    a1 = math.radians(angle1)
    a2 = math.radians(angle2)

    classical = (1 - (math.cos(a1)*math.cos(a2))**2 - (math.sin(a1)*math.sin(a2))**2)
    quantum = (math.sin(a2 - a1))**2

    classical_label.configure(text=f"Classical P(mismatch) = {classical:.6f}")
    quantum_label.configure(text=f"Quantum P(mismatch) = {quantum:.6f}")

def click(event):
    global dragging

    x1, y1 = angle_to_xy(angle1)
    x2, y2 = angle_to_xy(angle2)

    d1 = math.hypot(event.x - x1, event.y - y1)
    d2 = math.hypot(event.x - x2, event.y - y2)

    if d1 < 20:
        dragging = 1
    elif d2 < 20:
        dragging = 2

def drag(event):
    global angle1, angle2

    if dragging is None:
        return

    angle = xy_to_angle(event.x, event.y)

    if dragging == 1:
        angle1 = angle
    else:
        angle2 = angle

    draw()

def release(event):
    global dragging
    dragging = None

canvas.bind("<Button-1>", click)
canvas.bind("<B1-Motion>", drag)
canvas.bind("<ButtonRelease-1>", release)

draw()
root.mainloop()
