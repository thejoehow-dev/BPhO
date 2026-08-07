import sys
from pathlib import Path
import runpy

BASE_DIR = Path(getattr(sys, "_MEIPASS", Path(__file__).parent)) # fixes task 1 and 2 menu opening this when exe

if len(sys.argv) > 1: # will only run from task 1 or 2 menu
    code = {"task1_2D": BASE_DIR / "task 1" / "task1_2D.py",
            "task1_3D": BASE_DIR / "task 1" / "task1_3D.py",
            "task2_2D": BASE_DIR / "task 2" / "task2_2D.py",
            "task2_3D": BASE_DIR / "task 2" / "task2_3D.py"}

    if sys.argv[1] in code:
        runpy.run_path(code[sys.argv[1]], run_name="__main__")
        sys.exit()

import customtkinter
import importlib.util
#from pathlib import Path

root = customtkinter.CTk()
root.title("BPhO Computational Challenge - Quantum Mechanics - Joe Howlett & Kieran Ody 2026")
root.geometry("634x390")

buttons = []

dir = Path(__file__).parent

#modules = {}
for i in range(1, 11):
    path = dir / Path(f"task {i}") / f"task{i}.py"
    if not path.is_file(): continue
    spec = importlib.util.spec_from_file_location(f"task{i}", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    #modules[i] = module

    name = ["Random Walk", "Brownian Motion Simulation",
            "Blackbody Radiation", "Photoelectric Effect",
            "Hydrogen Spectra", "Electric Diffraction",
            "The Wave Equation and Uncertainty Principle",
            "Classical and Quantum Mismatch Probabilities",
            "Compton Scattering","Hydrogen Orbitals"]

    button = customtkinter.CTkButton(root, text = "Task "+str(i) + " - " + name[i-1], command = lambda f=module: f.main()) # add main func to ones with menu!
    button.pack(pady = 5)

    buttons.append(button)




root.mainloop()