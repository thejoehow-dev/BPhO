import customtkinter
import subprocess
import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def menu():
    root = customtkinter.CTk()
    root.title("Task 2 - Menu")
    root.geometry("250x100")
    root.resizable(width=False,height=False)

    space1 = customtkinter.CTkFrame(root, height=5,fg_color="transparent").pack()

    twoD_button = customtkinter.CTkButton(root,text="2D", command = lambda:  two_runner())
    twoD_button.pack()

    space2 = customtkinter.CTkFrame(root, height=10,fg_color="transparent").pack()

    threeD_button = customtkinter.CTkButton(root,text="3D", command = lambda: three_runner())
    threeD_button.pack()

    root.mainloop()

def run_task(name, file):
    if getattr(sys, "frozen", False): # if exe
        subprocess.Popen([sys.executable, name])
    else: subprocess.Popen([sys.executable, file])

def two_runner():
    run_task("task2_2D", os.path.join(BASE_DIR, "task2_2D.py"))

def three_runner():
    run_task("task2_3D", os.path.join(BASE_DIR, "task2_3D.py"))

def main(): menu()
if __name__ == "__main__": main()