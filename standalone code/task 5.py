import matplotlib.pyplot as plt
from matplotlib.patches import Patch

def wavelength(n,m):
    wavelength = (((m**-2) - (n**-2))**-1) * 91.13
    return wavelength

def energy(n,m):
    deltaEnergy = ((m**-2) - (n**-2)) * 13.6
    return deltaEnergy

def main():
    plt.figure() # to fix it overlapping with other graphs open
    ymax=13
    colourdict = {1: "magenta",
                  2: "orangered",
                  3: "blue",
                  4: "lime",
                  5: "grey"}
    namedict = {1: "Lyman",
                2: "Balmer",
                3: "Paschen",
                4: "Brackett",
                5: "Pfund"}
    key = []
    
    for m in range(1,6): # Lyman, Balmer, Paschen, Brackett, Pfund
        x = []
        y = []
        for n in range(m+1,10):
            x.append(wavelength(n,m))
            y.append(energy(n,m))
            plt.vlines(x[-1],0,ymax, colors=colourdict[m])
        plt.scatter(x,y, s=10, c=colourdict[m])
        key.append(Patch(facecolor=colourdict[m], label=namedict[m]))
    # graph setup
    plt.legend(handles=key, loc="upper right")
    ax = plt.gca()
    ax.set_xlabel("λ / nm")
    ax.set_ylabel("Photon Energy / eV")
    ax.axis((0,8000,0,ymax))
    plt.get_current_fig_manager().set_window_title("Task 5 - Hydrogen Spectra")
    plt.title("Bohr model of Hydrogenic atom photon emissions: Z = 1")
    plt.tight_layout()
    plt.show()


# so master file dosent auto run
if __name__ == "__main__":
    main()