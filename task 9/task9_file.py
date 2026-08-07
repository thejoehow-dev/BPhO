import numpy as np
import matplotlib.pyplot as plt
e = 1.602176620898e-19      # electron charge
c = 2.99792458e8            # speed of light
h = 6.62607004081e-34       # planck
me = 9.1093835611e-31       # electron mass
theta = np.linspace(0,180,1000)
thetar = np.radians(theta)
delta_l = (h / (me*c)) * (1 - np.cos(thetar))        # Δλ
def f(x):
    func = (-1/24 * x**5 + 1/2 * x**4 + -43/24 * x**3 + 5/2 * x**2 + -1/6 * x)      # gives 1,2,4,10,20
    E = func*50000*e    # 50,100,200,500,1000 keV
    l = h*c/E           # λ
    return l

# Δλ/λ
fig, ax = plt.subplots()
for i in range(1,6):
    l = f(i)
    plt.plot(theta, delta_l/l, label = "E=" + str(round(h*c/(50000*e*l)*50)) + "keV")
plt.title("Compton scattering of X-ray photon off an electron")
plt.get_current_fig_manager().set_window_title("Task 9 - Figure 1")
ax.set_xlabel("Photon scattering angle θ /degrees")
ax.set_ylabel("Δλ/λ")
plt.xlim(0,180)
plt.ylim(0,4)
plt.xticks([0,50,100,150,180])
plt.yticks([0,.5,1,1.5,2,2.5,3,3.5,4])
plt.grid(linewidth = .25)
plt.legend(loc="upper left")

# Electron recoil speed v/c
fig, ax = plt.subplots()
for i in range(1,6):
    l = f(i)
    v = np.sqrt(1 - ((me*c**2) / ((h*c/l) - (h*c/(delta_l+l)) + me*c**2))**2)
    plt.plot(theta, v, label = "E=" + str(round(h*c/(50000*e*l)*50)) + "keV")
    # horizontal 'max' lines
    v_max = np.linspace(np.max(v),np.max(v),1000)
    plt.plot(theta,v_max, color = "black", linewidth = .75)
plt.title("Compton scattering of X-ray photon off an electron")
plt.get_current_fig_manager().set_window_title("Task 9 - Figure 2")
ax.set_xlabel("Photon scattering angle θ /degrees")
ax.set_ylabel("Electron recoil speed v/c")
plt.xlim(0,180)
plt.ylim(0,1)
plt.xticks([0,50,100,150,180])
plt.yticks([0,.2,.4,.6,.8,1])
plt.grid(linewidth = .25)
plt.legend(loc="upper left")

# Electron recoil angle Φ /degrees
fig, ax = plt.subplots()
for i in range(1,6):
    l = f(i)
    phir = np.arctan((np.sin(thetar)) / (1 + ((h / (me*c*l)) * (1 - np.cos(thetar))) - np.cos(thetar)))
    phi = np.degrees(phir)
    plt.plot(theta, phi, label = "E=" + str(round(h*c/(50000*e*l)*50)) + "keV")
plt.title("Compton scattering of X-ray photon off an electron")
plt.get_current_fig_manager().set_window_title("Task 9 - Figure 3")
ax.set_xlabel("Photon scattering angle θ /degrees")
ax.set_ylabel("Electron recoil angle Φ /degrees")
plt.xlim(0,180)
plt.ylim(0,90)
plt.xticks([0,50,100,150,180])
plt.yticks([0,10,20,30,40,50,60,70,80,90])
plt.grid(linewidth = .25)
plt.legend(loc="upper right")
plt.show()