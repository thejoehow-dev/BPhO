
import numpy as np
import matplotlib.pyplot as plt

n = np.linspace(0,3,1000)   # quantum number
e = 1.602176620898e-19      # electron charge
me = 9.1093835611e-31       # electron mass
h = 6.62607004081e-34       # planck
h_bar = h/(2*np.pi)         # reduced planck
a = 5.2917711e-11           # average a for given E values



def E(n): # energy function of quantum number
    EJ = n**2 * h**2 / (8*me*a**2)
    EeV = EJ / e
    return EeV


def psi(n,x,t): # probability density function
    if x > 0 and x < a:
        y = np.sqrt(2/a) * np.exp(-1j*E(n)*t / h_bar) * np.sin(n*np.pi*x / a)
    elif x <= 0 or x >= a:
        y = 0
    return y


def main():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    ax1.plot(n,E(n), linestyle = "--", linewidth = .5, color = "blue")
    # plot 1,2,3 points
    points = np.linspace(1,3,3)
    ax1.plot(points,E(points), linestyle = "", marker = "x", color = "blue")

    ax1.set_xlabel("Quantum number")
    ax1.set_ylabel("Energy /eV")
    ax1.set_xlim(0,3)
    ax1.set_ylim(0,1400)
    ax1.set_xticks([0,1,2,3])
    ax1.set_yticks([0,200,400,600,800,1000,1200,1400])
    ax1.grid(linewidth = .25)


    # 2nd graph


    x = np.linspace(0, 1, 1000)
    for j in range (1,4):
        x_values = []
        y_values = []
        for i in range(0,len(x)):
            w = x.item(i)*1e-10
            x_values.append(w)
            y_values.append(psi(j,w,0)**2)
        if j == 3:
            E_lab = " E="
        else:
            E_lab = " E=  "
        ax2.plot(x_values,y_values, linewidth = 1, label = "n=" + str(j) + E_lab + str(round(E(j), 4)) + "eV")

    ax2.set_xlabel("x / Å")
    ax2.set_ylabel("Probability density")
    ax2.set_xlim(0,a)
    ax2.set_ylim(0,5.2e10)
    xticks = []
    for i in range(2,13):
        if i == 5 or i == 7 or i == 11:
            continue
        else:
            xticks.append(round(a*i/12, 13))
    ax2.set_xticks(xticks)
    yticks = [i/2*1e10 for i in range(0,9)]
    ax2.set_yticks(yticks)
    ax2.grid(linewidth = .3)
    ax2.legend(loc = "upper center")


    fig.suptitle(f"Particle in a box energy /eV\nm = " + str(round(me,35)) + "kg")
    plt.get_current_fig_manager().set_window_title("Task 7 - The Wave Equation and Uncertainty Principle")
    plt.tight_layout()
    plt.show()



if __name__ == "__main__": main()