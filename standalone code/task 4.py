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
        from base64 import b64decode
        self.battery_img = PhotoImage(data=b64decode(
            b'iVBORw0KGgoAAAANSUhEUgAABAAAAAMACAYAAAC6uhUNAAAFr2lUWHRYTUw6Y29tLmFkb2JlLnhtcAAAAAAAPD94cGFja2V0IGJlZ2luPSLvu78iIGlkPSJXNU0wTXBDZWhpSHpyZVN6TlRjemtjOWQiPz4KPHg6eG1wbWV0YSB4bWxuczp4PSJhZG9iZTpuczptZXRhLyIgeDp4bXB0az0iWE1QIENvcmUgNS41LjAiPgogPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4KICA8cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0iIgogICAgeG1sbnM6eG1wPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvIgogICAgeG1sbnM6cGhvdG9zaG9wPSJodHRwOi8vbnMuYWRvYmUuY29tL3Bob3Rvc2hvcC8xLjAvIgogICAgeG1sbnM6ZGM9Imh0dHA6Ly9wdXJsLm9yZy9kYy9lbGVtZW50cy8xLjEvIgogICAgeG1sbnM6ZXhpZj0iaHR0cDovL25zLmFkb2JlLmNvbS9leGlmLzEuMC8iCiAgICB4bWxuczp0aWZmPSJodHRwOi8vbnMuYWRvYmUuY29tL3RpZmYvMS4wLyIKICAgIHhtbG5zOnhtcE1NPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvbW0vIgogICAgeG1sbnM6c3RFdnQ9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZUV2ZW50IyIKICAgeG1wOkNyZWF0ZURhdGU9IjIwMjYtMDctMTdUMjA6MzI6MzErMDE6MDAiCiAgIHhtcDpNb2RpZnlEYXRlPSIyMDI2LTA3LTE3VDIyOjQ3OjA3KzAxOjAwIgogICB4bXA6TWV0YWRhdGFEYXRlPSIyMDI2LTA3LTE3VDIyOjQ3OjA3KzAxOjAwIgogICBwaG90b3Nob3A6RGF0ZUNyZWF0ZWQ9IjIwMjYtMDctMTdUMjA6MzI6MzErMDE6MDAiCiAgIHBob3Rvc2hvcDpDb2xvck1vZGU9IjMiCiAgIHBob3Rvc2hvcDpJQ0NQcm9maWxlPSJzUkdCIElFQzYxOTY2LTIu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AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADmbDF6AADM1N00TbejR8zR9v78T/8ft59P15u3i72MAYCQo9EDAAAAgMMTAAAAACBAAAAAAIAAAQAAAAACBAAAAAAIEAAAAAAgQAAAAACAAAEAAAAAAgQAAAAACFiOHgAAsIvTk+PVw/rs+7c3lzfPi//aAwBz4QIAAAAAAgQAAAAACBAAAAAAIEAAAAAAgAABAAAAAAIEAAAAAAgQAAAAACBAAAAAAIAAAQAAAAACBAAAAAAIEAAAAAAgQAAAAACAAAEAAAAAAgQAAAAACBAAAAAAIEAAAAAAgAABAAAAAAIEAAAAAAgQAAAAACBAAAAAAIAAAQAAAAACBAAAAAAIEAAAAAAgQAAAAACAAAEAAAAAAgQAAAAACBAAAAAAIEAAAAAAgAABAAAAAAIEAAAAAAgQAAAAACBAAAAAAIAAAQAAAAAClqMHAADs4v3j6/Vq/bIavQMA5sYFAAAAAAQIAAAAABAgAAAAAECAAAAAAAABAgAAAAAECAAAAAAQIAAAAABAgAAAAAAAAQIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAB/QDuwwST6FJIO4AAAAASUVORK5CYII='
        ))
        self.battery_img_flipped = self.battery_img.subsample(-1, 1)
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
    from base64 import b64decode
    bg = PhotoImage(data=b64decode(
        b'iVBORw0KGgoAAAANSUhEUgAABAAAAAMACAIAAAA12IJaAAAFr2lUWHRYTUw6Y29tLmFkb2JlLnhtcAAAAAAAPD94cGFja2V0IGJlZ2luPSLvu78iIGlkPSJXNU0wTXBDZWhpSHpyZVN6TlRjemtjOWQiPz4KPHg6eG1wbWV0YSB4bWxuczp4PSJhZG9iZTpuczptZXRhLyIgeDp4bXB0az0iWE1QIENvcmUgNS41LjAiPgogPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4KICA8cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0iIgogICAgeG1sbnM6eG1wPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvIgogICAgeG1sbnM6cGhvdG9zaG9wPSJodHRwOi8vbnMuYWRvYmUuY29tL3Bob3Rvc2hvcC8xLjAvIgogICAgeG1sbnM6ZGM9Imh0dHA6Ly9wdXJsLm9yZy9kYy9lbGVtZW50cy8xLjEvIgogICAgeG1sbnM6ZXhpZj0iaHR0cDovL25zLmFkb2JlLmNvbS9leGlmLzEuMC8iCiAgICB4bWxuczp0aWZmPSJodHRwOi8vbnMuYWRvYmUuY29tL3RpZmYvMS4wLyIKICAgIHhtbG5zOnhtcE1NPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvbW0vIgogICAgeG1sbnM6c3RFdnQ9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZUV2ZW50IyIKICAgeG1wOkNyZWF0ZURhdGU9IjIwMjYtMDctMTdUMjA6MzI6MzErMDE6MDAiCiAgIHhtcDpNb2RpZnlEYXRlPSIyMDI2LTA3LTE3VDIxOjUyOjIzKzAxOjAwIgogICB4bXA6TWV0YWRhdGFEYXRlPSIyMDI2LTA3LTE3VDIxOjUyOjIzKzAxOjAwIgogICBwaG90b3Nob3A6RGF0ZUNyZWF0ZWQ9IjIwMjYtMDctMTdUMjA6MzI6MzErMDE6MDAiCiAgIHBob3Rvc2hvcDpDb2xvck1vZGU9IjMiCiAgIHBob3Rvc2hvcDpJQ0NQcm9maWxlPSJzUkdCIElFQzYxOTY2LTIu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AAAAEIgAAACAQAQAAAAEIgAAACAQAQAAAIEIAAAACEQAAABAIAIAAAACEQAAABCIAAAAgEAEAAAABCIAAAAgEAEAAACBCAAAAAhEAAAAQCACAAAAAhEAAAAQiAAAAIBABAAAAAQiAAAAIBABAAAAgQgAAAAIRAAAAEAgAgAAAAIRAAAAEIgAAACAQAQAAAAEIgAAACAQAQAAAIEIAAAACEQAAABAIAIAAAACEQAAABCIAAAAgEAEAAAABCIAAAAgEAEAAACBCAAAAAhEAAAAQCACAAAAAhEAAAAQiAAAAIBABAAAAAQiAAAAIBABAAAAgQgAAAAIRAAAAEAgAgAAAAIRAAAAEIgAAACAQAQAAAAEIgAAACAQAQAAAIEIAAAACEQAAABAIAIAAAACEQAAABCIAAAAgEAEAAAABCIAAAAgEAEAAACBCAAAAAhEAAAAQCACAAAAAhEAAAAQiAAAAIBABAAAAAQiAAAAIBABAAAAgQgAAAAIpDr1AJzByrsvTz0CAAD9hx0AAAAIRAAAAEAgAgAAAAIRAAAAEIgAAACAQAQAAAAEIgAAACAQAQAAAIEIAAAACEQAAABAIAIAAAACEQAAABCIAAAAgEAEAAAABCIAAAAgEAEAAACBCAAAAAhEAAAAQCACAAAAAhEAAAAQiAAAAIBABAAAAAQiAAAAIBABAAAAgQgAAAAIRAAAAEAgAgAAAAIRAAAAEIgAAACAQArFYjH1DAAAQE7sAAAAQCACAAAAAhEAAAAQiAAAAIBABAAAAAQiAAAAIBABAAAAgQgAAAAIRAAAAEAgAgAAAAIRAAAAEIgAAACAQAQAAAAEIgAAACAQAQAAAIEIAAAACEQAAABAIAIAAAACEQAAABCIAAAAgEAEAAAABCIAAAAgEAEAAACBCAAAAAhEAAAAQCACAAAAAhEAAAAQiAAAAIBABAAAAAQiAAAAIBABAAAAgQgAAAAIRAAAAEAgAgAAAAIRAAAAEIgAAACAQAQAAAAEIgAAACAQAQAAAIEIAAAACEQAAABAIAIAAAACEQAAABCIAAAAgEAEAAAABCIAAAAgEAEAAACBCAAAAAhEAAAAQCACAAAAAhEAAAAQiAAAAIBABAAAAAQiAAAAIBABAAAAgQgAAAAIRAAAAEAg/x/J2+Pcyw0B2gAAAABJRU5ErkJggg=='
    ))

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