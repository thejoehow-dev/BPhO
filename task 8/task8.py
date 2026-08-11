import subprocess
import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def main():
    if getattr(sys, "frozen", False):
        subprocess.Popen([sys.executable, "task8_file"])
    else:
        subprocess.Popen([sys.executable, os.path.join(BASE_DIR, "task8_file.py")]) #runs the task 8 code like its not being ran again cus that finally broke things like in task 10

if __name__ == "__main__": main()