import matplotlib.pyplot as plt
import numpy as np
import customtkinter
from matplotlib.patches import Patch
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg 

def menu():
    root = customtkinter.CTk()
    root.title("Task 3 - Menu")
    root.geometry("250x100")
    root.resizable(width=False,height=False)

    space1 = customtkinter.CTkFrame(root, height=5,fg_color="transparent").pack()

    Planck_Spectrum_button = customtkinter.CTkButton(root,text="Plot Planck Sprectrum", command = lambda: ps())
    Planck_Spectrum_button.pack()

    space2 = customtkinter.CTkFrame(root, height=10,fg_color="transparent").pack()

    Einstein_Model_button = customtkinter.CTkButton(root,text="Plot Einstein's Model", command = lambda: em_menu(root))
    Einstein_Model_button.pack()

    root.mainloop()

def ps(): # plank spec.
    plt.figure()

    # constants
    h = 6.626e-34
    c = 2.998e8
    kB = 1.381e-23

    wavelength = np.linspace(0.1e-9, 2500e-9, 1000) # x   increase last number for more plots

    # graph axis formatting
    plt.title("Solar Irradiance vs Wavelength")
    plt.get_current_fig_manager().set_window_title("Task 3 - Solar Irradiance vs Wavelength")
    plt.axis((0,2500,0,10e4))
    plt.ticklabel_format(axis='y', style='sci', scilimits=(4, 4), useMathText=True)

    key = []

    for T,colour in [[4000, "lightblue" ],[5000, "sandybrown"],[6000, "wheat"]]:
        irradiance = ((np.pi * 2 * h * c**2) / wavelength**5) * (1 / (np.exp((h * c) / (wavelength * kB * T)) -1)) # multiplied by pi to go from rad. to irrad.
        
        plt.plot(wavelength * 1e9 ,irradiance * 1e-9, color=colour)

        key.append(Patch(facecolor=colour, label=str(T)+"K"))

    plt.legend(handles=key, loc="upper right") # adds key
    plt.xlabel("Wavelength / nm")
    plt.ylabel(r"Irradiance / Wm$^{-2}$ / nm")
    plt.show()


# einsteins model               #### steps to combine: pass root into function and use customtkinter.CTkToplevel(root) instead of customtkinter.CTk() , add grid configure

def em_menu(root):
    em_root = customtkinter.CTkToplevel(root)
    em_root.title("Task 3 - Einstein's model of solid molar heat capacity menu")
    em_root.geometry("950x525")
    em_root.grid_rowconfigure(0)
    em_root.grid_columnconfigure(1)

    # grid
    left = customtkinter.CTkFrame(em_root, width=200)
    left.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
    
    right = customtkinter.CTkFrame(em_root, fg_color="white")
    right.grid(row=0, column=1, sticky="nsew", padx=(0, 10), pady=10)

    # axis setup
    fig, ax = plt.subplots(figsize=(8, 5), dpi=100)

    #ax = plt.gca()
    ax.set_xlabel("Temperature / K")
    ax.set_ylabel(r"Molar Heat Capacity / Jmol$^{-1}$K$^{-1}$")
    ax.axis((0,800,0,26))
    ax.minorticks_on()
    ax.grid(which='major', color='black', linestyle='-', linewidth=0.25)
    ax.grid(which='minor', color='black', linestyle=':', linewidth=0.125)

    fig.suptitle("Molar Heat Capacity vs Temperature")
    fig.tight_layout()

    R = 8.314
    ax.plot([10,790],[3*R,3*R], linestyle = (0,(5,5)), color = "#222222", linewidth = 1.25) # dulong petit limit

    colourdict = {
    "Gold": "goldenrod",
    "Copper": "peru",
    "Titanium": "lightsteelblue",
    "Aluminium": "lightgrey",
    "Iron": "silver",
    "Silicon": "darkgrey",
    "Carbon": "black"}
        
    ax.legend(handles=[Patch(facecolor = c, label = n) for n, c in colourdict.items()], title = "Elements", loc = "lower right")

    canvas = FigureCanvasTkAgg(fig, master=right)
    canvas.draw()
    canvas.get_tk_widget().pack(fill = "both", expand = True, padx = 10, pady = (10, 0))

    element_label = customtkinter.CTkLabel(left, text = "Elements")
    element_label.pack(pady = (15,5))

    for element in ["Gold", "Copper", "Titanium", "Aluminium", "Iron", "Silicon", "Carbon"]:
        Switcher(left, element, ax, canvas, colourdict[element])

    em_root.mainloop()

class Switcher:
    def __init__(self, root, element, axis, canvas, colour):
        self.axis = axis
        self.canvas = canvas
        self.colour = colour

        self.toggle_var = customtkinter.BooleanVar(value=False)

        self.toggle = customtkinter.CTkSwitch(root, text=element, onvalue=True, offvalue=False, command=self.switch, variable=self.toggle_var)
        self.toggle.pack()
        
        fE = {
            "Gold": 0.2855,
            "Copper": 0.5769,
            "Titanium": 0.7054,
            "Aluminium": 0.7188,
            "Iron": 0.7893,
            "Silicon": 1.0832,
            "Carbon": 3.7451}[element] * 1e13
    
        self.T = np.linspace(0.1, 800, 1000)

        h = 6.626e-34
        c = 2.998e8
        kB = 1.381e-23
        R = 8.314
        
        x = (h * fE) / (kB * self.T)

        self.C = 3 * R * (((x**2) * (np.exp(x)))/(((np.exp(x)) -1)**2)) # molar heat capacity

    def switch(self):
        if self.toggle_var.get(): # if enabled plot
            self.plot = self.axis.plot(self.T,self.C, color=self.colour) # line

        else: # else remove all toggle stuff
            self.plot[0].remove()

        self.canvas.draw()





def main(): menu() # main is ran from the button from master

# so master file dosent auto run
if __name__ == "__main__" : main() 