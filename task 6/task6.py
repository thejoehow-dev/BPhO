import numpy as np
import matplotlib.pyplot as plt
#from matplotlib.patches import Patch
from matplotlib.lines import Line2D
#import matplotlib.cm as cm
#import matplotlib.colors as mcolors
import matplotlib.ticker as ticker

def main():
    h = 6.63e-34
    r = 65e-3
    m = 9.109e-31
    e = 1.6e-19

    colourarray = ["#004ce6", "#1743ea", "#2d39ee", "#432ff2", "#5925f6", "#6f1bf9", "#8410fb", "#9706fb", "#a800f8", "#b800f2", "#c600ea", "#d300df", "#de00d2", "#e700c2", "#ee00b0", "#f4009c", "#f80087", "#fa0070", "#fb0058", "#fb003f", "#f90024", "#f61100", "#f02c00", "#e64000"]
    
    maxn = []

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    V = np.linspace(1e3,5e3,50)
    for d in [0.123e-9, 0.213e-9]:
        maxn.append(int((2 * d * (2 * m * e * 5e3)**0.5) / h))
        for n in range (1,maxn[-1] + 1):
            x = ((2 * n * h * r) / d) * (2 * m * e * V)**-0.5
            if d == 0.123e-9: 
                ax1.plot(V,x, color = colourarray[n-1], linestyle = "solid")
                ax1.text(V[-1] + 50, x[-1], "n="+str(n), va='center', fontsize=6, color='#333333')
            else:
                ax2.plot(V,x, color = colourarray[n-1], linestyle = (0, (3, 1.5)))
                ax2.text(V[-1] + 50, x[-1], "n="+str(n), va='center', fontsize=6, color='#333333')


            #if n % 2 == 0 or n == 1 or n == 24: # Labels selected n to avoid overcrowding
            #    plt.text(
            #    V[-1] + 50, x[-1], f"n={n}", 
            #    va='center', fontsize=8, color='#333333'
            #    )
    
    #for n in range(1,max(maxn)+1):
    #    key.append(Patch(facecolor=colourarray[n-1], label=str("n="+str(n))))
    
    
    #plt.legend(handles=key, loc="upper right")   ######## make more compact and add -- and - lines


    #cmap = plt.colormaps['plasma']  # 'turbo', 'plasma', and 'viridis' are clear on white
    #norm = mcolors.Normalize(vmin=1, vmax=24)   
    #sm = cm.ScalarMappable(cmap=cmap, norm=norm)
    #sm.set_array([])
    #cbar = plt.colorbar(sm, ax=plt.gca(), pad=0.02)
    #cbar.set_label('Variant ($n$)')
    #cbar.set_ticks([1, 6, 12, 18, 24]) # Set neat tick increments



    #types = [Line2D([0], [0], color="grey", linestyle="solid", label="d=0.123e-9"), Line2D([0], [0], color="grey", linestyle="--", label="d=0.213e-9")]
    #plt.legend(handles=types, loc='upper right')

    ax1.legend(handles=[Line2D([0], [0], color="grey", linestyle="solid", label=r"$d = 0.123 \times 10^{-9}$")], loc="upper right")
    ax2.legend(handles=[Line2D([0], [0], color="grey", linestyle=(0, (3, 1.5)), label=r"$d = 0.213 \times 10^{-9}$")], loc="upper right")

    ax1.set_xlim(1e3, 5e3)
    ax1.set_ylim(0, 0.6)
    ax2.set_xlim(1e3, 5e3)
    ax2.set_ylim(0, 0.6)
    ax1.grid()
    ax2.grid()

    ax1.set_ylabel("Ring Radius / m")
    ax2.set_ylabel("\nRing Radius / m")
    ax1.set_xlabel("Voltage / V")
    ax2.set_xlabel("Voltage / V")
    fig.suptitle("Ring Radius vs Accelerating Voltage")
    plt.get_current_fig_manager().set_window_title("Task 6 - Electric Diffraction")

    plt.tight_layout()
    plt.show()




    part_a()


def part_a(): # check d values from gradient
    #print("A")

    h = 6.63e-34
    r = 65e-3
    m = 9.109e-31
    e = 1.6e-19

    colourarray = ["#004ce6", "#1743ea", "#2d39ee", "#432ff2", "#5925f6", "#6f1bf9", "#8410fb", "#9706fb", "#a800f8", "#b800f2", "#c600ea", "#d300df", "#de00d2", "#e700c2", "#ee00b0", "#f4009c", "#f80087", "#fa0070", "#fb0058", "#fb003f", "#f90024", "#f61100", "#f02c00", "#e64000"]
    
    maxn = []

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    V = np.linspace(1e3,5e3,50)
    y = V ** -0.5
    for d in [0.123e-9, 0.213e-9]:
        calc_d = []
        maxn.append(int((2 * d * (2 * m * e * 5e3)**0.5) / h))
        for n in range (1,maxn[-1] + 1):
            sin_theta = ((n * h) / (2 * d)) * (2 * m * e * V)**-0.5

            if d == 0.123e-9: 
                ax1.plot(sin_theta,y, color = colourarray[n-1], linestyle = "solid")
                ax1.text(sin_theta[0] - 0.04, y[0] + 0.0005, "n="+str(n), va='center', fontsize=6, color='#333333')
            else:
                ax2.plot(sin_theta,y, color = colourarray[n-1], linestyle = (0, (3, 1.5)))
                ax2.text(sin_theta[0] - 0.04, y[0] + 0.0005, "n="+str(n), va='center', fontsize=6, color='#333333')

            # calculate gradient

            dy_dx = np.polynomial.Polynomial.fit(sin_theta, y, 1).convert().coef[1] # does some polynominal fitting stuff to get gradient
            calc_d.append(((n * h * dy_dx)) / (2 * (2 * m * e)**0.5))

            print("calc d as",calc_d[-1])

        # display gradient

        text = ["Gradients:\n"]

        for i, d in enumerate(calc_d):
            n = i+1
            if n < 10: space = " " # makes it the same width    its a "figure space"
            else: space = ""
            text.append("n=" + str(n) + ": " + space + "{:.3g}e-9".format(calc_d[i] * 1e9)) # n=n: gradient to 3dp
            if i % 2 and i != len(calc_d)-1: # makes 2 wide and dosent add extra line at end
                text.append("\n")

        if d == 0.123e-9: # y = 0.085
            ax1.text(0.66, 0.01, " ".join(text), transform=ax1.transAxes, verticalalignment='bottom', fontsize=8, bbox=dict(boxstyle="round,pad=0.4", facecolor="white", alpha=0.9, edgecolor="grey"))
        else:
            ax2.text(0.66, 0.01, " ".join(text), transform=ax2.transAxes, verticalalignment='bottom', fontsize=8, bbox=dict(boxstyle="round,pad=0.4", facecolor="white", alpha=0.9, edgecolor="grey"))

# same as main part (kinda)

    ax1.legend(handles=[Line2D([0], [0], color="grey", linestyle="solid", label=r"$d = 0.123 \times 10^{-9}$")], loc="lower right", bbox_to_anchor=(0.985, 0.24))
    ax2.legend(handles=[Line2D([0], [0], color="grey", linestyle=(0, (3, 1.5)), label=r"$d = 0.213 \times 10^{-9}$")], loc="lower right", bbox_to_anchor=(0.985, 0.385))

    ax1.set_xlim(0, 2.3)
    ax1.set_ylim(min(y), max(y))
    ax2.set_xlim(0, 2.3)
    ax2.set_ylim(min(y), max(y))
    ax1.grid()
    ax2.grid()

    ax1.set_ylabel(r"$\mathrm{V}^{-1/2}$")
    ax2.set_ylabel("\n"+r"$\mathrm{V}^{-1/2}$")
    ax1.set_xlabel(r"$\sin\left(\frac{\phi}{2}\right)$")
    ax2.set_xlabel(r"$\sin\left(\frac{\phi}{2}\right)$")

    ax1.xaxis.set_major_locator(ticker.MultipleLocator(0.25))
    ax2.xaxis.set_major_locator(ticker.MultipleLocator(0.25))
    ax1.yaxis.set_major_locator(ticker.MultipleLocator(0.0025))
    ax2.yaxis.set_major_locator(ticker.MultipleLocator(0.0025))

    fig.suptitle(r"Checking values for d using $\left. \Delta \mathrm{V}^{-1/2} \right/ \Delta \sin\left(\frac{\phi}{2}\right)$")
    plt.get_current_fig_manager().set_window_title("Task 6 - Checking values for d")
    
    plt.tight_layout()
    plt.show()


if __name__ == "__main__": main()