import matplotlib.pyplot as plt
import numpy as np
import customtkinter
from matplotlib.patches import Patch
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  

class Switcher:
    def __init__(self, root, metal, axis, canvas, colour):
        self.axis = axis
        self.canvas = canvas
        self.colour = colour

        self.toggle_var = customtkinter.BooleanVar(value=False)

        self.toggle = customtkinter.CTkSwitch(root, text=metal, onvalue=True, offvalue=False, command=self.switch, variable=self.toggle_var)
        self.toggle.pack()

        self.work_function = {
            "Silver": 4.3,
            "Aluminium": 4.3,
            "Gold": 5.1,
            "Copper": 4.7,
            "Tin": 4.4,
            "Lead": 4.3,
            "Tungsten": 4.5,
            "Nickel": 4.6,
            "Sodium": 2.4}[metal]

        #print(self.work_function) ###

        self.f = np.linspace(0.1, 2E15, 1000)
        h = 6.63E-34    # plank's constant
        e = 1.6E-19     # charge of an electron
        self.v = ((h*self.f)/e)-self.work_function # voltage for each frequency
        #print("f",self.f) ###
        #print("v",self.v) ###

        self.threshold_frequency = (self.work_function * e)/h

    def switch(self):
        if self.toggle_var.get(): # if enabled plot
            self.work_plot = self.axis.scatter(0,-self.work_function, color=self.colour, marker="x") # work function
            self.threshold_frequency_plot = self.axis.scatter(self.threshold_frequency,0, color=self.colour, marker="x") # threshold frequency
            self.plot = self.axis.plot(self.f,self.v, color=self.colour) # line

        else: # else remove all dynamic elements
            self.plot[0].remove()
            self.work_plot.remove()
            self.threshold_frequency_plot.remove()

        self.canvas.draw()

def menu():
    root = customtkinter.CTk()
    root.title("Task 4 - Stopping Potential Menu")
    root.geometry("950x525")
    root.grid_rowconfigure(0)
    root.grid_columnconfigure(1)

    # grid
    left = customtkinter.CTkFrame(root, width=200)
    left.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    right = customtkinter.CTkFrame(root, fg_color="white")
    right.grid(row=0, column=1, sticky="nsew", padx=(0, 10), pady=10)
    
    # axis setup
    fig, ax1 = plt.subplots(figsize=(8, 5), dpi=100)
    #ax1 = plt.gca()
    ax2 = ax1.twiny()
    ax2.set_xticks([])
    ax2.spines['bottom'].set_position('zero')
    ax1.set_xlabel("Frequency / Hz")
    ax1.set_ylabel("Stopping Voltage / V ")
    ax1.axis((0,2E15,-6,3))
    ax1.minorticks_on()
    ax1.grid(which='major', color='black', linestyle='-', linewidth=0.25)
    ax1.grid(which='minor', color='black', linestyle=':', linewidth=0.125)

    fig.suptitle("Stopping Voltage vs Frequency")
    fig.tight_layout()

    colourdict = {
        "Silver": "silver",
        "Aluminium": "lightgrey",
        "Gold": "goldenrod",
        "Copper": "peru",
        "Tin": "darkgrey",
        "Lead": "dimgrey",
        "Tungsten": "slategrey",
        "Nickel": "lightsteelblue",
        "Sodium": "darkorange"}

    ax1.legend(handles=[Patch(facecolor = c, label = n) for n, c in colourdict.items()], title = "Metals", loc = "lower right") # try ax2 if broken

    canvas = FigureCanvasTkAgg(fig, master=right)
    canvas.draw()
    canvas.get_tk_widget().pack(fill = "both", expand = True, padx = 10, pady = (10, 0))

    metal_label = customtkinter.CTkLabel(left, text = "Metals")
    metal_label.pack(pady = (15,5))

    for metal in ["Silver","Aluminium","Gold","Copper","Tin","Lead","Tungsten","Nickel","Sodium"]:
        Switcher(left, metal, ax1, canvas, colourdict[metal])

    #### extension stuff

    ex_button = customtkinter.CTkButton(left, text = "Extension\nAnimation", command = lambda: extension(), width = 100) ### add "lambda:" before finishing!
    ex_button.pack(pady = 25, padx = 2)

    root.mainloop()


class Battery:    
    def __init__(self, canvas, sizex, sizey, direction = 0): # direction of poiny bit (positive) 0 is left and 1 is right
        self.canvas, self.direction = canvas, direction
        from pathlib import Path
        from tkinter import PhotoImage
        self.battery_img = PhotoImage(file=str(Path(__file__).parent / "battery.png"))
        self.battery_img_flipped = PhotoImage(file=str(Path(__file__).parent / "battery_flipped.png"))
        self.battery = self.canvas.create_image(int(sizex/2), int(sizey/2), image=self.battery_img)
        if self.direction != 0: self.flip()

    def flip(self, direction = None):
        #print("Flipping!")
        if direction != self.direction:
            self.direction = not self.direction # flipping code
            if self.direction: self.canvas.itemconfig(self.battery, image=self.battery_img_flipped)
            else: self.canvas.itemconfig(self.battery, image=self.battery_img)

#def checkflip(battery, voltage):
#    if voltage.get() > 0: battery.flip(0)
#    elif voltage.get() < 0: battery.flip(1)

def change_metal(selected, canvas, metal_rect, electrons):
    #print("CHANGED to", selected.get()) ####
    colourdict = {
    "Silver": "silver",
    "Aluminium": "lightgrey",
    "Gold": "goldenrod",
    "Copper": "peru",
    "Tin": "darkgrey",
    "Lead": "dimgrey",
    "Tungsten": "slategrey",
    "Nickel": "lightsteelblue",
    "Sodium": "darkorange"}
    canvas.itemconfig(metal_rect, fill = colourdict[selected.get()]) # changed rect colour
    for electron in electrons:
        canvas.delete(electron.id)


class Electron:
    def __init__(self, canvas, voltage, KE):
        self.canvas, self.KE = canvas, KE
        from random import randint
        self.size = 15
        y = randint(217,426-self.size)
        self.id = self.canvas.create_oval(240,y,240+self.size,y+self.size, fill="DodgerBlue2")
        self.updatecurrentvoltage(voltage.get())
        self.drift()

    def drift(self):
        self.energy = self.KE + self.voltage # v to make it proport. and + v as it follows conv. current
        v = self.energy * 2
        self.canvas.move(self.id, v, 0)
        if self.canvas.coords(self.id)[0] >= 785 or self.canvas.coords(self.id)[0] <= 240: self.canvas.delete(self.id) # if on other side delete
        else: self.canvas.after(20, self.drift) # else repeat

    def updatecurrentvoltage(self, voltage):
        self.voltage = voltage
        
        
def updatevoltage(value, voltage_text, voltage, battery, electrons):
    voltage.set(value)

    for electron in electrons:
        # refresh
        electron.updatecurrentvoltage(voltage.get())

    # flipper
    if voltage.get() > 0: battery.flip(0)
    elif voltage.get() < 0: battery.flip(1)

    if int(value) == value: value = int(value) # removes .0
    voltage_text.configure(text=(value, "V"))

def updatewavelength(value, wavelength_text, wavelength):
    wavelength.set(value)
    wavelength_text.configure(text=("Wavelength:", int(value), "nm"))

def updateintensity(value, intensity_text, intensity):
    intensity.set(value)
    intensity_text.configure(text=("Intensity:", int(value * 100), "%"))

def spawn(canvas, wavelength, electrons, selected, intensity, voltage):
    from random import random
    energy = (6.63e-34*3e8)/(wavelength.get() * 1e-9) / 1.6e-19 # in ev to compare with work function

    work_function = {
            "Silver": 4.3,
            "Aluminium": 4.3,
            "Gold": 5.1,
            "Copper": 4.7,
            "Tin": 4.4,
            "Lead": 4.3,
            "Tungsten": 4.5,
            "Nickel": 4.6,
            "Sodium": 2.4}[selected.get()]

    if energy > work_function and intensity.get() != 0:
            if 1.2 * intensity.get() * (energy - work_function) > random():
                electrons.append(Electron(canvas, voltage, KE=energy-work_function))

    delay = max(20, 200-int(intensity.get()*200)) # always more than 20ms but decreases with intensity, add randomness? 

    canvas.after(delay, lambda: spawn(canvas, wavelength, electrons, selected, intensity, voltage))

def extension():
    electrons = []
    #print("EXTENSION")
    from tkinter import PhotoImage, Canvas

    ex = customtkinter.CTkToplevel()
    sizex, sizey = 1024,768
    ex.geometry((str(sizex))+"x"+str(sizey))
    ex.title("Task 4 - Animation")
    ex.resizable(width=False,height=False)
    
    # find bg file
    from pathlib import Path
    from tkinter import PhotoImage
    bg = PhotoImage(file=str(Path(__file__).parent / "statics.png"))

    canvas = Canvas(ex, width=sizex, height=sizey, highlightthickness=0)
    canvas.place(x=0,y=0)
    canvas.create_image(int(sizex/2), int(sizey/2), image=bg) 

    battery = Battery(canvas, sizex, sizey)

    # battery labels and slider
    voltage = customtkinter.DoubleVar(value = 0)

    voltage_text = customtkinter.CTkLabel(canvas, text="0 V", text_color="black", width=45)
    canvas.create_window(sizex/2,sizey-75, window=voltage_text)
    
    voltage_slider = customtkinter.CTkSlider(canvas, command = lambda value:updatevoltage(value, voltage_text, voltage, battery, electrons), width=100, height=20, from_=-10, to=10, number_of_steps=40)
    canvas.create_window(sizex/2,sizey-52, window=voltage_slider)

    # switcher
    metal_rect = canvas.create_rectangle(229,217,240,426, fill="", outline="")

    selected = customtkinter.StringVar(value="Silver")
    metal_switcher = customtkinter.CTkSegmentedButton(canvas, values=["Silver","Aluminium","Gold","Copper","Tin","Lead","Tungsten","Nickel","Sodium"], variable=selected, command = lambda value:change_metal(selected, canvas, metal_rect, electrons))
    change_metal(selected, canvas, metal_rect, electrons) # does silver first on load so no no metal
    
    canvas.create_window(sizex/2,50, window=metal_switcher)

    # wavelength stuff
    wavelength = customtkinter.DoubleVar(value = 500)

    wavelength_text = customtkinter.CTkLabel(canvas, text=("Wavelength:", int(wavelength.get()), "nm"), text_color="black", width=100)
    canvas.create_window(sizex/3,sizey-210,window=wavelength_text)

    wavelength_slider = customtkinter.CTkSlider(canvas, command = lambda value:updatewavelength(value, wavelength_text, wavelength), width=250, height=20, from_=100, to=900, number_of_steps=800)
    canvas.create_window(sizex/3,sizey-180,window=wavelength_slider)

    # intensity
    intensity = customtkinter.DoubleVar(value = .5)

    intensity_text = customtkinter.CTkLabel(canvas, text=("Intensity:", int(intensity.get() * 100), "%"), text_color="black", width=100)
    canvas.create_window(2 * sizex/3,sizey-210,window=intensity_text)

    intensity_slider = customtkinter.CTkSlider(canvas, command = lambda value:updateintensity(value, intensity_text, intensity), width=250, height=20, from_=0, to=1, number_of_steps=100)
    canvas.create_window(2 * sizex/3,sizey-180,window=intensity_slider)
 
    spawn(canvas, wavelength, electrons, selected, intensity, voltage)

    ex.mainloop()



def main(): 
    plt.figure() # just here for first run to fix overriding other tasks, add this line into other tasks if they override something
    menu()

# so master file dosent auto run
if __name__ == "__main__" : main() 