import customtkinter as ctk
import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# physical constants
e = 1.602176620898e-19          # electron charge
c = 2.99792458e8                # speed of light
h = 6.62607004081e-34           # planck
me = 9.1093835611e-31           # electron mass

theta = np.linspace(0, 180, 1000)
thetar = np.radians(theta)
delta_l = (h / (me * c)) * (1 - np.cos(thetar))

def main():
    root = ctk.CTkToplevel() # fixes entry being weird
    run(root)

def run(root):
    root.title("Task 9 - Compton Scattering")
    root.geometry("1400x900")

    controls = ctk.CTkFrame(root)
    controls.pack(side="left", fill="y", padx=10, pady=10)

    ctk.CTkLabel(controls, text=f"Compton Scattering", font=("Arial", 24, "bold")).pack(pady=(15,15))
    ctk.CTkLabel(controls, text="Photon Energy", font=("Arial", 18)).pack(pady=(20,0))

    energy_label = ctk.CTkLabel(controls, text="500 keV", font=("Arial", 18))
    energy_label.pack(pady=(0,10))
    energy_var = tk.DoubleVar(value=500)
    slider_frame = ctk.CTkFrame(controls, fg_color="transparent")
    slider_frame.pack(fill="x")

    def validate_integer(text):
        try:
            value = float(text)
            return 0 < value and text.isdigit()
        except ValueError:
            return False

    max_frame = ctk.CTkFrame(controls, fg_color="transparent")
    max_frame.pack(fill="x", padx=15)
    ctk.CTkLabel(max_frame, text="Set Maximum E / keV ").pack(side="left")
    max_var = tk.StringVar(value="1000")
    set_max_entry = ctk.CTkEntry(max_frame, textvariable=max_var, width=120, validate="key", validatecommand=(root.register(validate_integer), "%P"))
    set_max_entry.pack(side="right")

    slider = ctk.CTkSlider(slider_frame, from_=0.001, to=1000, variable=energy_var, number_of_steps=int(max_var.get()))
    slider.pack(fill="x", padx=20, pady=(0,10))

    def update_height_max(*args):
        new_max = int(set_max_entry.get())
        slider.configure(to=new_max)
        if slider.get() > new_max:
            slider.set(new_max)
            energy_label.configure(text=f"{new_max}")
        energy_var.set(slider.get())
        update_graphs()

    set_max_entry.bind("<Return>", update_height_max)

    def toggle_comparison():
        nonlocal comparison_mode # fixes not defined
        comparison_mode = not comparison_mode

        if comparison_mode:
            compare_button.configure(text="Return to Slider")
            slider.configure(state="disabled")
            set_max_entry.configure(state="disabled")

        else:
            compare_button.configure(text="Show Standard Energies")
            slider.configure(state="normal")
            set_max_entry.configure(state="normal")

        update_graphs()

    compare_button = ctk.CTkButton(controls, text="Show Standard Energies", command=toggle_comparison)
    compare_button.pack(pady=20)

    fig = plt.Figure(figsize=(11, 8))

    ax1 = fig.add_subplot(221)
    ax2 = fig.add_subplot(222)
    ax3 = fig.add_subplot(212)

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().pack(side="right", fill="both", expand=True)

    comparison_mode = False

    def update_graphs(*args):
        ax1.clear()
        ax2.clear()
        ax3.clear()

        if comparison_mode:
            energies = [50, 100, 200, 500, 1000]
        else:
            energies = [energy_var.get()]
            energy_label.configure(text=f"{energy_var.get():.0f} keV")

        for E_keV in energies:

            E = E_keV * 1000 * e
            l = h * c / E

            # Δλ/λ
            ax1.plot(theta, delta_l/l, label=f"{E_keV:.0f} keV")

            # recoil speed
            v = np.sqrt(1 - ((me*c**2) /((h*c/l) - (h*c/(delta_l+l)) + me*c**2))**2)

            ax2.plot(theta, v, label=f"{E_keV:.0f} keV")
            ax2.axhline(np.max(v), color="black", linewidth=0.5)

            # recoil angle
            phir = np.arctan(np.sin(thetar) /(1 + (h/(me*c*l))*(1-np.cos(thetar)) - np.cos(thetar)))
            phi = np.degrees(phir)

            ax3.plot(theta, phi, label=f"{E_keV:.0f} keV")

        ax1.set_title("Fractional Wavelength Shift")
        ax1.set_xlabel("Photon scattering angle θ / °")
        ax1.set_ylabel("Δλ / λ")
        ax1.set_xlim(0,180)
        ax1.set_ylim(0,4) if comparison_mode else ax1.set_ylim(0, int(max_var.get())/250)
        ax1.grid(alpha=0.3)

        ax2.set_title("Electron Recoil Speed")
        ax2.set_xlabel("Photon scattering angle θ / °")
        ax2.set_ylabel("v / c")
        ax2.set_xlim(0,180)
        ax2.set_ylim(0,1)
        ax2.grid(alpha=0.3)

        ax3.set_title("Electron Recoil Angle")
        ax3.set_xlabel("Photon scattering angle θ / °")
        ax3.set_ylabel("Φ / °")
        ax3.set_xlim(0,180)
        ax3.set_ylim(0,90)
        ax3.grid(alpha=0.3)

        if comparison_mode:
            ax1.legend()

        #fig.tight_layout() # makes it really laggy AND makes sizes jump on load
        canvas.draw_idle()

    slider.configure(command=update_graphs)

    update_graphs()
    fig.tight_layout() # isnt laggy here

    if root != ctk.CTkToplevel():
        root.mainloop()

if __name__ == "__main__": run(root = ctk.CTk())