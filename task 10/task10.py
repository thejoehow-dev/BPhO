import subprocess
import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def main():
    if getattr(sys, "frozen", False):
        subprocess.Popen([sys.executable, "task10_file"])
    else:
        subprocess.Popen([sys.executable, os.path.join(BASE_DIR, "task10_file.py")]) #runs the task 10 code like its not being ran again cus that broke things

if __name__ == "__main__": main()