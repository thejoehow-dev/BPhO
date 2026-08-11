import numpy as np
import matplotlib.pyplot as plt

n = np.linspace(0,3,1000)   # quantum number
e = 1.602176620898e-19      # electron charge
m = 9.1093835611e-31        # electron mass
h = 6.62607004081e-34       # planck
h_bar = h/(2*np.pi)         # reduced planck
a = 5.2917711e-11           # average a for given E values

# # QM3,2ii
# m = 1.67262192e-27          # proton mass
# a = 0.47e-15                # box width

def E(n,m,a): # energy function of quantum number
    EJ = n**2 * h**2 / (8*m*a**2)
    EeV = EJ / e
    return EeV


def psi(n,x,t): # probability density function
    if x > 0 and x < a:
        y = np.sqrt(2/a) * np.exp(-1j*E(n,m,a)*t / h_bar) * np.sin(n*np.pi*x / a)
    elif x <= 0 or x >= a:
        y = 0
    return y


def main():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    ax1.plot(n,E(n,m,a), linestyle = "--", linewidth = .5, color = "blue")

    # plot 1,2,3 points
    points = np.linspace(1,3,3)
    ax1.plot(points,E(points,m,a), linestyle = "", marker = "x", color = "blue")

    ax1.set_xlabel("Quantum number")
    ax1.set_ylabel("Energy /eV")
    
    ax1.set_xlim(0,3)
    ymax = 1400*E(3,m,a)/E(3,9.1093835611e-31,5.2917711e-11)
    ax1.set_ylim(0,ymax)
    
    ax1.set_xticks([0,1,2,3])
    yticks = []
    for i in range(8):
        yticks.append(ymax*i/7)
    ax1.set_yticks(yticks)
    
    ax1.grid(linewidth = .25)


    # 2nd graph


    x = np.linspace(0, a, 1000)
    for j in range (1,4):
        x_values = []
        y_values = []
        for i in range(0,len(x)):
            w = x.item(i)*1e10
            x_values.append(w)
            y_values.append((abs(psi(j,w/1e10,0)))**2)
        E_ = E(j,m,a)
        if E(1,m,a) < 1:
            E_ *= 1e3
            units = "meV"
        elif E(1,m,a) < 1e3:
            units = "eV"
        elif E(1,m,a) < 1e6:
            E_ /= 1e3
            units = "keV"
        elif E(1,m,a) < 1e9:
            E_ /= 1e6
            units = "MeV"
        elif E(1,m,a) >= 1e9:
            E_ /= 1e9
            units = "GeV"
        if E_ >= 1e3:
            E_lab = " E="
        else:
            E_lab = " E=  "
        ax2.plot(x_values,y_values, linewidth = 1, label = "n=" + str(j) + E_lab + str(round(E_, 4)) + units)

    ax2.set_xlabel("x / Å")
    ax2.set_ylabel("Probability density")
    
    scale = 5.2917721e-11/a             # changes axes, graph looks identical
    ax2.set_xlim(0,a*1e10)
    ax2.set_ylim(0,scale*5.2e10)
    
    xticks = [0]
    for i in range(2,13):
        if i == 5 or i == 7 or i == 11:
            continue
        else:
            xticks.append(a*1e10*i/12)
    ax2.set_xticks(xticks)

    yticks = []
    for i in range(0,9):
        yticks.append(scale*1e10*i/2)
    ax2.set_yticks(yticks)
    
    ax2.grid(linewidth = .3)
    ax2.legend(loc = "upper center")


    fig.suptitle(f"Particle in a box energy /eV\nm = " + str(round(m,35)) + "kg")
    plt.get_current_fig_manager().set_window_title("Task 7 - The Wave Equation and Uncertainty Principle")
    fig.tight_layout()
    if __name__ == "__main__":
        plt.show()
    else:
        fig.show()



if __name__ == "__main__": main()
