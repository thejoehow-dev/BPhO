import numpy as np
import math
import matplotlib.pyplot as plt
import customtkinter as ctk
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.special import sph_harm_y
from mpl_toolkits.mplot3d import Axes3D
from mayavi import mlab
### ------------- you may need to install pyqt5 for mayavi to work! ------------- ###

r = np.linspace(0,200,50000)       # radius in Angstroms

# initial values
Z = 6       # proton number
A = 12      # atomic mass in u
n = 4       # principal quantum number
L = 2       # orbital quantum number
m = 0       # magnetic quantum number

# physical constants
e0 = 8.854187817e-12            # permittivity of free space / Fm^-1
h = 6.6260755e-34               # Planck's constant / Js
qe = 1.60217733e-19             # charge on electron / C
me = 9.1093897e-31              # mass of electron / kg
u = 1.6605402e-27               # unified mass constant (1/12 mass of Carbon-12 atom) / kg

# orbital lettering
L_dict = {0:"S", 1:"P", 2:"D", 3:"F", 4:"G"}

def update_quantities(*args):
    global Z, A, n, L, m, x_plane, y_plane, z_plane, a0, mu, a, r_mean, E

    Z = int(Z_var.get())
    A = int(A_var.get())
    n = int(n_var.get())
    L = int(L_var.get().split()[0])
    m = m_var.get()

    if plane_var.get() == "x-plane":
        x_plane = plane_slider.get()
    elif plane_var.get() == "y-plane":
        y_plane = plane_slider.get()
    elif plane_var.get() == "z-plane":
        z_plane = plane_slider.get()

    a0 = (e0*h**2)/(np.pi*me*qe**2)     # Bohr radius / m
    a0 *= 1e10                          # / Angstroms
    mu = me*A*u / (me+A*u)              # reduced mass
    a = me*a0 / (mu*Z)                  # hydrogenic atom radius

    r_mean = (a/2)*(3*n**2-L*(L+1))

    plane_slider.configure(from_=-1.5*r_mean, to=1.5*r_mean)

    refresh_display()

    E = -mu*(qe**4)*(Z**2) /  (8*(e0**2)*(h**2)*(n**2))         # total energy / J
    E /= qe                                                     # / eV

# radial wavefunction
def R(r):
    def laguerre(x,L,n):
        degree = n-L-1
        alpha = 2*L+1

        y = np.zeros_like(x, dtype=float)

        for k in range(degree + 1):
            coeff = ((-1)**k *
                math.factorial(degree + alpha) /
                (math.factorial(degree-k) *
                math.factorial(alpha+k) *
                math.factorial(k)))
            y += coeff * x**k

        return y

    x = 2*r / (a*n)
    w1 = np.sqrt( (math.factorial(n-L-1)) / (2*n*(math.factorial(n+L))) )
    w2 = (2/(a*n)) ** 1.5
    w3 = (x**L) * np.exp(-x/2)
    w4 = laguerre(x,L,n)
    y = w1*w2*w3*w4
    
    return(y)

# angular wavefunction
def omega(theta,phi):
    m1 = math.floor(m)
    m2 = math.ceil(m)

    m1 = max(-L, min(L, m1))
    m2 = max(-L, min(L, m2))

    t = m-m1

    def real_orbital(m_value):
        Y = sph_harm_y(L, abs(m_value), theta, phi)

        if m_value > 0:
            return np.sqrt(2) * np.real(Y)
        elif m_value < 0:
            return np.sqrt(2) * np.imag(Y)
        else:
            return np.real(Y)

    angular1 = real_orbital(m1)
    angular2 = real_orbital(m2)

    angular = (1-t)*angular1 + t*angular2

    return angular

# dropdowns

def update_A_menu(*args):
    global A
    update_quantities()
    values = [str(i) for i in range(Z, 295)]
    A_menu.configure(values=values)
    if A < Z:
        A_var.set(str(Z))
        A = Z

def update_L_menu(*args):
    global n,L
    n = int(n_var.get())
    max_L = min(4,n-1)
    values = [f"{i} ({L_dict[i]})" for i in range(max_L+1)]
    L_menu.configure(values=values)
    if L > max_L:
        L_var.set(f"{max_L} ({L_dict[max_L]})")
        L = max_L
    update_m_menu()

def update_m_menu(*args):
    global m, L
    L = int(L_var.get().split()[0])
    m_slider.configure(from_=-L, to=L, number_of_steps = 500)

    if m < -L:
        m = -L
        m_label.configure(text=f"m = {-L:.2f}")
    elif m > L:
        m = L
        m_label.configure(text=f"m = {L:.2f}")

    m_var.set(m)
    update_quantities()
    update_m_buttons()

def set_m(value):
    global m, m_animation_direction

    m_var.set(value)
    m_label.configure(text=f"m = {value:.2f}")

    if value >= 0:
        m_animation_direction = 1
    else:
        m_animation_direction = -1

    m = value
    refresh_display()

def update_m_buttons():
    global m_buttons

    for b in m_buttons:
        b.destroy()
    m_buttons.clear()

    for value in range(-L, L+1):
        button = ctk.CTkButton(m_button_frame, text=str(value), width=32, command=lambda v=value: set_m(v))
        button.pack(side="left", padx=2)
        m_buttons.append(button)

def update_m_slider(value):
    global m
    m_var.set(value)
    m_label.configure(text=f"m = {value:.2f}")
    m = value
    refresh_display()

def animate_m_slider():
    global m_animation_direction
    if not animate_m:
        return
    
    if L == 0:
        root.after(30, animate_m_slider)
        return

    step = 0.05
    value = m + m_animation_direction * step

    if value >= L:
        value = L
        m_animation_direction = -1
    elif value <= -L:
        value = -L
        m_animation_direction = 1

    m_slider.set(value)
    update_m_slider(value)

    root.after(30, animate_m_slider)

def toggle_m_animation():
    global animate_m
    animate_m = not animate_m

    if animate_m:
        animate_m_button.configure(text="Stop m")
        animate_m_slider()
    else:
        animate_m_button.configure(text="Animate m")

def plane_changed(*args):
    if plane_var.get() == "x-plane":
        plane_slider.configure(variable=x_plane_var)
        plane_label.configure(text=f"{float(x_plane):.2f} Å")
    elif plane_var.get() == "y-plane":
        plane_slider.configure(variable=y_plane_var)
        plane_label.configure(text=f"{float(y_plane):.2f} Å")
    elif plane_var.get() == "z-plane":
        plane_slider.configure(variable=z_plane_var)   
        plane_label.configure(text=f"{float(z_plane):.2f} Å")
    zero_plane_button.configure(text=f"{plane_var.get()[0]} = 0")
    animate_plane_button.configure(text=f"Animate {plane_var.get()[0]}-plane")
    refresh_display()

def update_plane_slider(value):
    global x_plane, y_plane, z_plane

    if plane_var.get() == "x-plane":
        x_plane_var.set(value)
        x_plane = value
        refresh_display()

    elif plane_var.get() == "y-plane":
        y_plane_var.set(value)
        y_plane = value
        refresh_display()

    elif plane_var.get() == "z-plane":
        z_plane_var.set(value)
        z_plane = value
        refresh_display()

    plane_label.configure(text=f"{float(value):.2f} Å")

def animate_plane_slider():
    global x_animation_direction, y_animation_direction, z_animation_direction

    min = float(plane_slider.cget("from_"))
    max = float(plane_slider.cget("to"))
    step = (max-min) / 150

    if plane_var.get() == "x-plane":
        if not animate_x:
            return

        value = x_plane + x_animation_direction * step

        if value >= max:
            value = max
            x_animation_direction = -1
        elif value <= min:
            value = min
            x_animation_direction = 1

    elif plane_var.get() == "y-plane":
        if not animate_y:
            return

        value = y_plane + y_animation_direction * step

        if value >= max:
            value = max
            y_animation_direction = -1
        elif value <= min:
            value = min
            y_animation_direction = 1

    elif plane_var.get() == "z-plane":
        if not animate_z:
            return

        value = z_plane + z_animation_direction * step

        if value >= max:
            value = max
            z_animation_direction = -1
        elif value <= min:
            value = min
            z_animation_direction = 1

    plane_slider.set(value)
    update_plane_slider(value)

    root.after(30, animate_plane_slider)

def toggle_plane_animation():
    global animate_x, animate_y, animate_z

    if plane_var.get() == "x-plane":
        animate_x = not animate_x
        if animate_x:
            animate_plane_button.configure(text="Stop x-plane")
            animate_plane_slider()
        else:
            animate_plane_button.configure(text="Animate x-plane")

    elif plane_var.get() == "y-plane":
        animate_y = not animate_y
        if animate_y:
            animate_plane_button.configure(text="Stop y-plane")
            animate_plane_slider()
        else:
            animate_plane_button.configure(text="Animate y-plane")

    elif plane_var.get() == "z-plane":
        animate_z = not animate_z
        if animate_z:
            animate_plane_button.configure(text="Stop z-plane")
            animate_plane_slider()
        else:
            animate_plane_button.configure(text="Animate z-plane")

def zero_plane():
    global x_plane, y_plane, z_plane, x_animation_direction, y_animation_direction, z_animation_direction

    if plane_var.get() == "x-plane":
        x_plane_var.set(0)
        x_plane = 0
        x_animation_direction = 1
        refresh_display()

    elif plane_var.get() == "y-plane":
        y_plane_var.set(0)
        y_plane = 0
        y_animation_direction = 1
        refresh_display()
    
    elif plane_var.get() == "z-plane":
        z_plane_var.set(0)
        z_plane = 0
        z_animation_direction = 1
        refresh_display()

    plane_label.configure(text="0.00 Å")

def validate_integer(text):
    try:
        value = float(text)
        return 0 < value and text.isdigit()
    except ValueError:
        return False

def validate_decimal(text):
    if text == "":
        return True
    try:
        value = float(text)
        return 0 <= value <= 1
    except ValueError:
        return False

def validate_decimal_not_equal(text):
    if text == "":
        return False
    try:
        value = float(text)
        return 0 < value < 1
    except ValueError:
        return False

def get_resol(*args):
    global plane_resol, threeD_resol, surf_resol
    if current_view == "plane" or current_view == "contour":
        plane_resol = int(resol_var.get())
    elif current_view == "3D":
        threeD_resol = int(resol_var.get())
    elif current_view == "surface":
        surf_resol = int(resol_var.get())

def swap_resol(*args):
    if current_view == "plane" or current_view == "contour":
        resol_var.set(str(plane_resol))
        resol_interp_title.configure(text = "Colormap - Plane Slice")
    elif current_view == "3D":
        resol_var.set(str(threeD_resol))
        resol_interp_title.configure(text = "Colormap - 3D Plot")
    elif current_view == "surface":
        resol_var.set(str(surf_resol))
        resol_interp_title.configure(text="Colormap - Plane Surface Plot")

def get_interp(*args):
    global plane_interp, threeD_interp, surf_interp
    if current_view == "plane" or current_view == "contour":
        plane_interp = int(interp_var.get())
    elif current_view == "3D":
        threeD_interp = int(interp_var.get())
    elif current_view == "surface":
        surf_interp = int(interp_var.get())

def swap_interp(*args):
    if current_view == "plane" or current_view == "contour":
        interp_var.set(str(plane_interp))
    elif current_view == "3D":
        interp_var.set(str(threeD_interp))
    elif current_view == "surface":
        interp_var.set(str(surf_interp))

def get_contour_color():
    global contour_color
    if contour_color_mode.get() == "Greyscale":
        contour_color = "Greys"
    elif contour_color_mode.get() == "Color":
        contour_color = "jet"

def update_height_slider(value):
    height_label.configure(text=f"{float(value):.1f}")
    if current_view == "surface":
        update_surface_plot()

def set_height(value):
    height_scale_var.set(value)
    height_label.configure(text=f"{value:.1f}")
    if current_view == "surface":
        update_surface_plot()

def update_height_max(*args):
    new_max = float(height_max_entry.get())
    height_slider.configure(to=new_max)
    if height_slider.get() > new_max:
        height_slider.set(new_max)
        height_label.configure(text=f"{new_max:.1f}")
    height_scale_var.set(height_slider.get())

def update_global_density_max():
    global cached_global_max

    N = 70

    plot_radius = 1.5*r_mean

    coords = np.linspace(-plot_radius, plot_radius, N)
    X, Y, Zcoord = np.meshgrid(coords, coords, coords, indexing="ij")
    Rgrid = np.sqrt(X**2 + Y**2 + Zcoord**2)
    theta = np.zeros_like(Rgrid)
    mask = Rgrid > 0
    theta[mask] = np.arccos(Zcoord[mask]/Rgrid[mask])
    phi = np.arctan2(Y, X)

    # full wavefunction = radial * angular
    psi = R(Rgrid)**2 * omega(theta,phi)

    cached_global_max = np.max(np.abs(psi)**2)

def update_plot():
    global current_view, ax
    current_view = "radial"
    
    fig.clear()
    ax = fig.add_subplot(111)

    ax.plot(r, R(r)**2 / np.max(R(r)**2), label="Normalised radial wavefunction density |R(r)|²")
    ax.plot(r, r**2 * R(r)**2 / np.max(r**2 * R(r)**2), label="Normalised radial probability distribution r²|R(r)|²")

    ax.set_xlabel("Radius / Å")
    ax.set_ylabel("Peak-Normalised Value")

    ax.set_xlim(0, 2.5*r_mean)
    ax.set_ylim(0, 1.1)
    ax.grid(linewidth=0.3)
    ax.legend()

    ax.set_title(f"Hydrogenic Atom\nZ={int(Z)}, A={(A)}, orbital {int(n)}{L_dict[int(L)]}")

    canvas.draw()

def update_plane_slice():
    global current_view, ax
    current_view = "plane"
    update_global_density_max()

    swap_resol()
    N = int(resol_var.get())

    plot_radius = 1.5*r_mean

    coords = np.linspace(-plot_radius, plot_radius, N)

    if plane_var.get() == "x-plane":
        Y, Zcoord = np.meshgrid(coords, coords)
        X = np.full_like(Y, plane_slider.get())
    elif plane_var.get() == "y-plane":
        X, Zcoord = np.meshgrid(coords, coords)
        Y = np.full_like(X, plane_slider.get())
    elif plane_var.get() == "z-plane":
        X, Y = np.meshgrid(coords, coords)
        Zcoord = np.full_like(X, plane_slider.get())

    Rgrid = np.sqrt(X**2 + Y**2 + Zcoord**2)
    theta = np.pi/2*np.ones_like(Rgrid)
    mask = Rgrid > 0
    theta[mask] = np.arccos(Zcoord[mask]/Rgrid[mask])
    phi = np.arctan2(Y, X)

    # full wavefunction = radial * angular
    psi = R(Rgrid)**2 * omega(theta,phi)

    density = np.abs(psi)**2
    if normalise_mode.get() == "Plane":
        density /= np.max(density)
    else:
        density /= cached_global_max

    fig.clear()
    ax = fig.add_subplot(111)

    swap_interp()

    image = ax.imshow(density, extent=[coords.min(), coords.max(), coords.min(), coords.max()], origin="lower", cmap=plt.get_cmap("rainbow", max(1, int(interp_var.get() if interp_var.get() else 0))), vmin=0, vmax=1)

    label = "Plane Normalised Probability Density" if normalise_mode.get() == "Plane" else "Globally Normalised Probability Density"
    fig.colorbar(image, ax=ax, label=label)

    if plane_var.get() == "x-plane":
        ax.set_xlabel("y / Å")
        ax.set_ylabel("z / Å")

    elif plane_var.get() == "y-plane":
        ax.set_xlabel("x / Å")
        ax.set_ylabel("z / Å")

    elif plane_var.get() == "z-plane":
        ax.set_xlabel("x / Å")
        ax.set_ylabel("y / Å")

    ax.set_title(f"{plane_var.get()[0]}={float(plane_slider.get()):.2f}Å plane\nZ={int(Z)}, A={int(A)}, orbital {int(n)}{L_dict[int(L)]}, m={m:.2f}\n{label}")

    canvas.draw()

def update_3D_plot(*args):
    global current_view, ax
    current_view = "3D"

    plot_radius = 1.5*r_mean

    swap_resol()
    N = max(1, int(resol_var.get()) if resol_var.get() else 0)

    coords = np.linspace(-plot_radius, plot_radius, N)

    X,Y,Zcoord = np.meshgrid(coords,coords,coords, indexing="ij")
    Rgrid = np.sqrt(X**2 + Y**2 + Zcoord**2)

    theta = np.zeros_like(Rgrid)
    mask = Rgrid > 0
    theta[mask] = np.arccos(Zcoord[mask]/Rgrid[mask])
    phi = np.arctan2(Y, X)

    # full wavefunction = radial * angular
    psi = R(Rgrid)**2 * omega(theta,phi)

    density = np.abs(psi)**2
    density /= density.max()

    visible = density > float(threshold_var.get())

    fig.clear()
    ax = fig.add_subplot(111, projection="3d")

    swap_interp()

    points = ax.scatter(X[visible], Y[visible], Zcoord[visible], c=density[visible], cmap=plt.get_cmap("jet", max(1, int(interp_var.get() if interp_var.get() else 0))), vmin=0.15, vmax=1.0, s=1, alpha=1)

    fig.colorbar(points, ax=ax, label="Probability Density")
    points.set_alpha(0.15)

    ax.set_box_aspect([1,1,1])
    ax.set_xlim(-plot_radius,plot_radius)
    ax.set_ylim(-plot_radius,plot_radius)
    ax.set_zlim(-plot_radius,plot_radius)
    ax.set_xlabel("x / Å")
    ax.set_ylabel("y / Å")
    ax.set_zlabel("z / Å")

    ax.set_title(f"Z={int(Z)}, A={int(A)}, orbital {int(n)}{L_dict[int(L)]}, E={E:.4f} eV\nm={m:.2f}")

    canvas.draw()

def update_contour_plot(*args):
    global current_view
    current_view = "contour"
    update_global_density_max()

    plot_radius = 1.5*r_mean

    swap_resol()
    N = int(resol_var.get())

    coords = np.linspace(-plot_radius, plot_radius, N)

    if plane_var.get() == "x-plane":
        Y, Zcoord = np.meshgrid(coords, coords)
        X = np.full_like(Y, plane_slider.get())
    elif plane_var.get() == "y-plane":
        X, Zcoord = np.meshgrid(coords, coords)
        Y = np.full_like(X, plane_slider.get())
    elif plane_var.get() == "z-plane":
        X, Y = np.meshgrid(coords, coords)
        Zcoord = np.full_like(X, plane_slider.get())

    Rgrid = np.sqrt(X**2 + Y**2 + Zcoord**2)
    theta = np.pi/2*np.ones_like(Rgrid)
    mask = Rgrid > 0
    theta[mask] = np.arccos(Zcoord[mask]/Rgrid[mask])
    phi = np.arctan2(Y, X)

    # full wavefunction = radial * angular
    psi = R(Rgrid)**2 * omega(theta,phi)

    density = np.abs(psi)**2
    if normalise_mode.get() == "Plane":
        density /= np.max(density)
    else:
        density /= cached_global_max

    fig.clear()
    ax = fig.add_subplot(111)

    lines = int(lines_number_var.get()) if lines_number_var.get() else 0

    levels = np.linspace(0,1,lines+1)
    if find_contour_var.get() and float(find_contour_var.get()) not in levels:
        index = np.searchsorted(levels, float(find_contour_var.get()))
        levels = np.insert(levels, index, float(find_contour_var.get()))

    get_contour_color()
    swap_interp()

    label = "Plane Normalised Probability Density" if normalise_mode.get() == "Plane" else "Globally Normalised Probability Density"
    label_contours = "Plane Normalised Probability Density" if normalise_mode.get() == "Plane" else "Globally Normalised Probability Density"

    if contour_background_mode.get() == "Plane Slice":
        background = ax.imshow(density, extent=[coords.min(), coords.max(), coords.min(), coords.max()], origin="lower", cmap=plt.get_cmap("rainbow", max(1, int(interp_var.get() if interp_var.get() else 0))), vmin=0, vmax=1)
        label_contours = "Plane Normalised Probability Density - Contours" if normalise_mode.get() == "Plane" else "Globally Normalised Probability Density - Contours"
        label_background = "Plane Normalised Probability Density - Backdrop" if normalise_mode.get() == "Plane" else "Globally Normalised Probability Density - Backdrop"
        fig.colorbar(background, ax=ax, label=label_background)
    elif contour_background_mode.get() == "Light":
        ax.set_facecolor("white")
    elif contour_background_mode.get() == "Dark":
        ax.set_facecolor("black")

    ax.set_aspect("equal")

    if plane_var.get() == "x-plane":
        ax.set_xlabel("y / Å")
        ax.set_ylabel("z / Å")
        contours = ax.contour(Y, Zcoord, density, levels=levels, cmap=contour_color, linewidths=1)

    elif plane_var.get() == "y-plane":
        ax.set_xlabel("x / Å")
        ax.set_ylabel("z / Å")
        contours = ax.contour(X, Zcoord, density, levels=levels, cmap=contour_color, linewidths=1)

    elif plane_var.get() == "z-plane":
        ax.set_xlabel("x / Å")
        ax.set_ylabel("y / Å")
        contours = ax.contour(X, Y, density, levels=levels, cmap=contour_color, linewidths=1)

    fig.colorbar(contours, ax=ax, label=label_contours, ticks=levels)

    ax.set_title(f"{plane_var.get()[0]}={float(plane_slider.get()):.2f}Å plane\nZ={int(Z)}, A={int(A)}, orbital {int(n)}{L_dict[int(L)]}, m={m:.2f}\n{label}")

    canvas.draw()

def update_surface_plot():
    global current_view
    current_view = "surface"
    update_global_density_max()

    swap_resol()
    N = max(1, int(resol_var.get()) if resol_var.get() else 0)

    plot_radius = 1.5*r_mean

    coords = np.linspace(-plot_radius, plot_radius, N)

    if plane_var.get() == "x-plane":
        Y, Zcoord = np.meshgrid(coords, coords)
        X = np.full_like(Y, plane_slider.get())
    elif plane_var.get() == "y-plane":
        X, Zcoord = np.meshgrid(coords, coords)
        Y = np.full_like(X, plane_slider.get())
    elif plane_var.get() == "z-plane":
        X, Y = np.meshgrid(coords, coords)
        Zcoord = np.full_like(X, plane_slider.get())

    Rgrid = np.sqrt(X**2 + Y**2 + Zcoord**2)
    theta = np.pi/2*np.ones_like(Rgrid)
    mask = Rgrid > 0
    theta[mask] = np.arccos(Zcoord[mask]/Rgrid[mask])
    phi = np.arctan2(Y, X)

    # full wavefunction = radial * angular
    psi = R(Rgrid)**2 * omega(theta,phi)

    density = np.abs(psi)**2
    if normalise_mode.get() == "Plane":
        density /= np.max(density)
    else:
        density /= cached_global_max

    fig.clear()
    ax = fig.add_subplot(111, projection="3d")

    height_scale = 1/height_scale_var.get()

    label = "Plane Normalised Probability Density" if normalise_mode.get() == "Plane" else "Globally Normalised Probability Density"

    swap_interp()

    ax.set_zlim(0,height_scale)
    if plane_var.get() == "x-plane":
        ax.set_xlabel("y / Å")
        ax.set_ylabel("z / Å")
        surface = ax.plot_surface(Y, Zcoord, density, cmap=plt.get_cmap("rainbow", max(1, int(interp_var.get() if interp_var.get() else 0))), linewidth=0, antialiased=True, vmin=0, vmax=1)

    elif plane_var.get() == "y-plane":
        ax.set_xlabel("x / Å")
        ax.set_ylabel("z / Å")
        surface = ax.plot_surface(X, Zcoord, density, cmap=plt.get_cmap("rainbow", max(1, int(interp_var.get() if interp_var.get() else 0))), linewidth=0, antialiased=True, vmin=0, vmax=1)

    elif plane_var.get() == "z-plane":
        ax.set_xlabel("x / Å")
        ax.set_ylabel("y / Å")
        surface = ax.plot_surface(X, Y, density, cmap=plt.get_cmap("rainbow", max(1, int(interp_var.get() if interp_var.get() else 0))), linewidth=0, antialiased=True, vmin=0, vmax=1)

    fig.colorbar(surface, ax=ax, label=label)
    ax.set_zlabel(label)

    ax.set_title(f"{plane_var.get()[0]}={float(plane_slider.get()):.2f}Å plane\nZ={int(Z)}, A={int(A)}, orbital {int(n)}{L_dict[int(L)]}, m={m:.2f}\n{label}")

    canvas.draw()

def update_mayavi_plot():
    N = int(mayavi_resol_var.get())

    plot_radius = 1.5 * r_mean

    coords = np.linspace(-plot_radius, plot_radius, N)
    X, Y, Zcoord = np.meshgrid(coords, coords, coords, indexing="ij")

    Rgrid = np.sqrt(X**2 + Y**2 + Zcoord**2)
    theta = np.zeros_like(Rgrid)
    mask = Rgrid > 0
    theta[mask] = np.arccos(Zcoord[mask] / Rgrid[mask])
    phi = np.arctan2(Y, X)

    psi = R(Rgrid)**2 * omega(theta, phi)

    density = np.abs(psi)**2
    density /= density.max()

    mlab.close(all=True)

    mlab.figure(f"Z={int(Z)}, A={int(A)}, orbital {int(n)}{L_dict[int(L)]}, E={E:.4f} eV\nm={m:.2f}", bgcolor=(0.1,0.1,0.1), size=(900,900))

    src = mlab.pipeline.scalar_field(X, Y, Zcoord, density)
    levels = np.linspace(float(threshold_var.get()), 1, int(mayavi_layers_var.get())+1)

    contour = None
    contour = mlab.pipeline.iso_surface(src, contours=[l for l in levels], opacity=0.5, colormap="jet", vmin=0, vmax=1)

    mlab.colorbar(contour, title="Probability Density", orientation="vertical", nb_labels=11)
    mlab.axes(src, xlabel='x / Å', ylabel='y / Å', zlabel='z / Å', ranges=[-plot_radius, plot_radius, -plot_radius, plot_radius, -plot_radius, plot_radius], nb_labels=5)
    mlab.orientation_axes()
    mlab.show()

def refresh_display(*args):
    if current_view == "radial":
        update_plot()
    elif current_view == "plane":
        update_plane_slice()
    elif current_view == "3D":
        update_3D_plot()
    elif current_view == "surface":
        update_surface_plot()
    elif current_view == "contour":
        update_contour_plot()

root = ctk.CTk()
root.title("Probability Densities of a Hydrogenic Atom")
root.geometry("1100x700")

# figure
fig, ax = plt.subplots(figsize=(8, 6))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side="right", fill="both", expand=True, padx=10, pady=10)
current_view = "radial"

# left panel
controls = ctk.CTkFrame(root, width = 320)
controls.pack(side="left", fill="y", padx=15)
ctk.CTkLabel(controls, text=f"Probability Densities\nof a Hydrogenic Atom", font=("Arial", 24, "bold")).pack(pady=(0,15))
controls.pack_propagate(False)

# Z
Z_row = ctk.CTkFrame(controls, fg_color="transparent")
Z_row.pack(fill="x", padx=15, pady=(0,5))
ctk.CTkLabel(Z_row, text="Atomic Number (Z)", width=100, anchor="w").pack(side="left")
Z_var = tk.StringVar(value=str(Z))
Z_menu = ctk.CTkOptionMenu(Z_row, variable=Z_var, values=[str(i) for i in range(1,119)], width=100)
Z_menu.pack(side="right")

# A
A_row = ctk.CTkFrame(controls, fg_color="transparent")
A_row.pack(fill="x", padx=15, pady=(0,5))
ctk.CTkLabel(A_row, text="Mass Number (A)", width = 100, anchor="w").pack(side="left")
A_var = tk.StringVar(value=str(A))
A_menu = ctk.CTkOptionMenu(A_row, variable=A_var, values=[], width=100)
A_menu.pack(side="right")

# n
n_row = ctk.CTkFrame(controls, fg_color="transparent")
n_row.pack(fill="x", padx=15, pady=(0,5))
ctk.CTkLabel(n_row, text="Principal Quantum Number (n)").pack(side="left")
n_var = tk.StringVar(value=str(n))
n_menu = ctk.CTkOptionMenu(n_row, variable=n_var, values=[str(i) for i in range(1, 6)], width=100)
n_menu.pack(side="right")

# L
L_row = ctk.CTkFrame(controls, fg_color="transparent")
L_row.pack(fill="x", padx=15, pady=(0,5))
ctk.CTkLabel(L_row, text="Orbital Quantum Number (L)").pack(side="left")
L_options = ["0 (S)", "1 (P)", "2 (D)", "3 (F)", "4 (G)"]
L_var = tk.StringVar(value="2 (D)")
L_menu = ctk.CTkOptionMenu(L_row, variable=L_var, values=L_options, width=100)
L_menu.pack(side="right")

# m
m_title_row = ctk.CTkFrame(controls, fg_color="transparent")
m_title_row.pack(fill="x", padx=15)
ctk.CTkLabel(m_title_row, text="Magnetic Quantum Number (m)").pack(side="left")
m_var = tk.DoubleVar(value=0)
m_slider = ctk.CTkSlider(controls, from_=-L, to=L, number_of_steps=2*L if L > 0 else 1, variable=m_var)
m_slider.pack(fill="x", padx=15)
m_label = ctk.CTkLabel(controls, text="m = 0.00")
m_label.pack()

# m quick select
m_button_frame = ctk.CTkFrame(controls, fg_color="transparent")
m_button_frame.pack(pady=(0,20))
m_buttons = []

# x,y,z-plane slider
plane_frame = ctk.CTkFrame(controls, fg_color="transparent")
plane_frame.pack(fill="x", padx=15)
plane_title_frame = ctk.CTkFrame(plane_frame, fg_color="transparent")
plane_title_frame.pack(fill="x", pady=(0,5))
plane_var = tk.StringVar(value="z-plane")
plane_menu = ctk.CTkOptionMenu(plane_title_frame, values=["x-plane","y-plane","z-plane"], variable=plane_var, width=100, command=plane_changed)
plane_menu.pack(side="left")
plane_menu.configure()
zero_plane_button = ctk.CTkButton(plane_title_frame, text="z = 0", command=zero_plane, width=70)
zero_plane_button.pack(side="left", padx=(10,0))

x_plane = 0
y_plane = 0
z_plane = 0
x_plane_var = tk.DoubleVar(value=0)
y_plane_var = tk.DoubleVar(value=0)
z_plane_var = tk.DoubleVar(value=0)
plane_slider = ctk.CTkSlider(plane_frame, from_=-1, to=1, variable=z_plane_var)
plane_slider.pack(fill="x", padx=15)
plane_label = ctk.CTkLabel(plane_frame, text="0.00 Å")
plane_label.pack()

m_slider.configure(command=update_m_slider)
plane_slider.configure(command=update_plane_slider)

animate_m = False
m_animation_direction = 1
animate_x = False
x_animation_direction = 1
animate_y = False
y_animation_direction = 1
animate_z = False
z_animation_direction = 1

cached_global_max = None
mayavi_fig = None
mayavi_points = None

# initialise menus
update_A_menu()
update_L_menu()

Z_menu.configure(command=update_A_menu)
A_menu.configure(command=update_quantities)
n_menu.configure(command=update_L_menu)
L_menu.configure(command=update_m_menu)

resol_interp_frame = ctk.CTkFrame(controls, fg_color="transparent", border_width=.5)
resol_interp_frame.pack(fill="x", padx=15, pady=(0,10))
resol_interp_title = ctk.CTkLabel(resol_interp_frame, text="Colormap - Plane Slice")
resol_interp_title.pack(pady=(.5,0))

# colormap resolution

resol_frame = ctk.CTkFrame(resol_interp_frame, fg_color="transparent")
resol_frame.pack(side="left", padx=(15,0), pady=(0,10))
ctk.CTkLabel(resol_frame, text="Resolution").pack()
resol_var = tk.StringVar(value="500")
resol_entry = ctk.CTkEntry(resol_frame, textvariable=resol_var, width=120, validate="key", validatecommand=(root.register(validate_integer), "%P"))
resol_entry.pack()

plane_resol = 500
threeD_resol = 100
surf_resol = 1000

resol_var.trace_add("write", get_resol)
resol_entry.bind("<Return>", refresh_display)

# colormap interpolation

interp_frame = ctk.CTkFrame(resol_interp_frame, fg_color="transparent")
interp_frame.pack(side="right", padx=(0,15), pady=(0,10))
ctk.CTkLabel(interp_frame, text="Interpolation").pack()
interp_var = tk.StringVar(value="100")
interp_entry = ctk.CTkEntry(interp_frame, textvariable=interp_var, width=120, validate="key", validatecommand=(root.register(validate_integer), "%P"))
interp_entry.pack()

plane_interp = 100
threeD_interp = 100
surf_interp = 100

interp_var.trace_add("write", get_interp)
interp_entry.bind("<Return>", refresh_display)

normalise_frame = ctk.CTkFrame(controls, fg_color="transparent")
normalise_frame.pack(fill="x", padx=15, pady=(0,5))
ctk.CTkLabel(normalise_frame, text="Probability Normalised Across").pack(side="left", padx=(0,15))
normalise_mode = tk.StringVar(value="Global")
normalise_menu = ctk.CTkOptionMenu(normalise_frame, values=["Global", "Plane"], variable=normalise_mode, width=120, command=refresh_display)
normalise_menu.pack(side="right")

threshold_frame = ctk.CTkFrame(controls, fg_color="transparent")
threshold_frame.pack(fill="x", padx=15, pady=(0,10))
ctk.CTkLabel(threshold_frame, text="3D Plot Minimum Threshold").pack(side="left")
threshold_var = tk.StringVar(value="0.15")
threshold_entry = ctk.CTkEntry(threshold_frame, textvariable=threshold_var, width=50, validate="key", validatecommand=(root.register(validate_decimal_not_equal), "%P"))
threshold_entry.pack(side="right")
threshold_entry.bind("<Return>", update_3D_plot)
threshold_entry.bind("<FocusOut>", update_3D_plot)

plots_row = ctk.CTkFrame(controls, fg_color="transparent", border_width=1, border_color="white")
plots_row.pack(fill="x", padx=15, pady=(0,15))

ctk.CTkButton(plots_row, text="Radial Graph", command=update_plot, width=90, height=35).pack(side="left", padx=(5,0), pady=5)

ctk.CTkButton(plots_row, text="3D Plot", command=update_3D_plot, width=90, height=35).pack(side="right", padx=(0,5), pady=5)

ctk.CTkButton(plots_row, text="Plane Slice", command=update_plane_slice, width=90, height=35).pack(pady=5)

contour_surf_frame = ctk.CTkFrame(controls, fg_color="transparent")
contour_surf_frame.pack(padx=5)

contour_frame = ctk.CTkFrame(contour_surf_frame, fg_color="transparent")
contour_frame.pack(side="left", anchor="n")

ctk.CTkButton(contour_frame, text="Iso-Probability Contours", command=update_contour_plot, width=150, height=35).pack()

background_lines_frame = ctk.CTkFrame(contour_frame, fg_color="transparent", width=200)
background_lines_frame.pack()

lines_number_frame = ctk.CTkFrame(background_lines_frame, fg_color="transparent")
lines_number_frame.pack(fill="x", pady=5)
ctk.CTkLabel(lines_number_frame, text="Number of Contours").pack(side="left")
lines_number_var = tk.StringVar(value="10")
lines_number_entry = ctk.CTkEntry(lines_number_frame, textvariable=lines_number_var, width=45, validate="key", validatecommand=(root.register(validate_integer), "%P"))
lines_number_entry.pack(side="right")
lines_number_entry.bind("<Return>", update_contour_plot)
lines_number_entry.bind("<FocusOut>", update_contour_plot)

lines_frame = ctk.CTkFrame(background_lines_frame, fg_color="transparent")
lines_frame.pack(fill="x")
ctk.CTkLabel(lines_frame, text="Lines").pack(side="left", anchor="w")
contour_color_mode = tk.StringVar(value="Greyscale")
ctk.CTkOptionMenu(lines_frame, values=["Greyscale", "Color"], variable=contour_color_mode, width=100, command=refresh_display).pack(side="right", anchor="e")

background_frame = ctk.CTkFrame(background_lines_frame, fg_color="transparent")
background_frame.pack(fill="x", pady=5)
ctk.CTkLabel(background_frame, text="Backdrop").pack(side="left")
contour_background_mode = tk.StringVar(value="Plane Slice")
ctk.CTkOptionMenu(background_frame, values=["Plane Slice", "Light", "Dark"], variable=contour_background_mode, width=100, command=refresh_display).pack(side="right")

find_contour_frame = ctk.CTkFrame(background_lines_frame, fg_color="transparent")
find_contour_frame.pack(fill="x", pady=(0,10))
ctk.CTkLabel(find_contour_frame, text="Find Contour Value ").pack(side="left", anchor="w")
find_contour_var = tk.StringVar(value="0.00")
find_contour_entry = ctk.CTkEntry(find_contour_frame, textvariable=find_contour_var, width=50, validate="key", validatecommand=(root.register(validate_decimal), "%P"))
find_contour_entry.pack()
find_contour_entry.bind("<Return>", update_contour_plot)
find_contour_entry.bind("<FocusOut>", update_contour_plot)

surf_frame = ctk.CTkFrame(contour_surf_frame, fg_color="transparent")
surf_frame.pack(side="right", anchor="n")
ctk.CTkButton(surf_frame, text="Plane Surface Plot", command=update_surface_plot, width=150, height=35).pack()
ctk.CTkLabel(surf_frame, text="Height Scale").pack()
height_scale_var = tk.DoubleVar(value=1.0)
height_max_var = tk.StringVar(value="5")
height_slider = ctk.CTkSlider(surf_frame, from_=0.01, to=int(height_max_var.get()), variable=height_scale_var)
height_slider.pack(fill="x", padx=15)
height_label = ctk.CTkLabel(surf_frame, text="1.0")
height_label.pack(pady=(0,0))
height_slider.configure(command=update_height_slider)

height_one_button = ctk.CTkButton(surf_frame, text="1", command=lambda v=1: set_height(v), width=32)
height_one_button.pack()
height_one_button.configure(update_surface_plot())

height_max_frame = ctk.CTkFrame(surf_frame, fg_color="transparent")
height_max_frame.pack(fill="x", padx=5, pady=(3.5,0))
ctk.CTkLabel(height_max_frame, text="Scale Maximum ").pack(side="left")
height_max_entry = ctk.CTkEntry(height_max_frame, textvariable=height_max_var, width=50, validate="key", validatecommand=(root.register(validate_integer), "%P"))
height_max_entry.pack(side="right")
height_max_entry.bind("<Return>", update_height_max)

mayavi_frame1 = ctk.CTkFrame(controls, fg_color="transparent", border_width=.5)
mayavi_frame1.pack(fill="x")

mayavi_frame2 = ctk.CTkFrame(mayavi_frame1, fg_color="transparent")
mayavi_frame2.pack(fill="x", padx=15)

ctk.CTkButton(mayavi_frame2, text="Mayavi 3D", command=update_mayavi_plot, width=90, height=35).pack(side="right", pady=5)

mayavi_entry_frame = ctk.CTkFrame(mayavi_frame2, fg_color="transparent")
mayavi_entry_frame.pack(side="left")

mayavi_resol_row = ctk.CTkFrame(mayavi_entry_frame, fg_color="transparent")
mayavi_resol_row.pack(fill="x")
ctk.CTkLabel(mayavi_resol_row, text="Mayavi 3D Resolution ").pack(side="left", anchor="w")
mayavi_resol_var = tk.StringVar(value="120")
mayavi_resol_entry = ctk.CTkEntry(mayavi_resol_row, textvariable=mayavi_resol_var, width=50, validate="key", validatecommand=(root.register(validate_integer), "%P"))
mayavi_resol_entry.pack(side="right", anchor="e")

mayavi_layers_row = ctk.CTkFrame(mayavi_entry_frame, fg_color="transparent")
mayavi_layers_row.pack(fill="x", pady=5)
ctk.CTkLabel(mayavi_layers_row, text="Mayavi 3D Layers ").pack(side="left", anchor="w")
mayavi_layers_var = tk.StringVar(value="100")
mayavi_layers_entry = ctk.CTkEntry(mayavi_layers_row, textvariable=mayavi_layers_var, width=50, validate="key", validatecommand=(root.register(validate_integer), "%P"))
mayavi_layers_entry.pack(side="right", anchor="e")

animate_m_button = ctk.CTkButton(m_title_row, text="Animate m", command=toggle_m_animation, width=100, border_width=1, border_color="white")
animate_m_button.pack(side="right")

animate_plane_button = ctk.CTkButton(plane_title_frame, text="Animate z-plane", command=toggle_plane_animation, width=100, border_width=1, border_color="white")
animate_plane_button.pack(side="right")

ctk.CTkLabel(mayavi_frame1, text="Controls cannot be updated when Mayavi 3D is open").pack()

# Initial plot
update_plot()

root.mainloop()