import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# from scipy.optimize import minimize

parent_dir = Path(__file__).parent / "float_nofloat"

# import data
disk4_fl_path = parent_dir / "disk_4_float.csv"
disk4_fl = np.loadtxt(disk4_fl_path, delimiter=",", skiprows=1)

disk5_fl_path = parent_dir / "disk_5_float.csv"
disk5_fl = np.loadtxt(disk5_fl_path, delimiter=",", skiprows=1)

disk7_fl_path = parent_dir / "disk_7_float.csv"
disk7_fl = np.loadtxt(disk7_fl_path, delimiter=",", skiprows=1)

disk4_no_path = parent_dir / "disk_4_nofloat.csv"
disk4_no = np.loadtxt(disk4_no_path, delimiter=",", skiprows=1)

disk5_no_path = parent_dir / "disk_5_nofloat.csv"
disk5_no = np.loadtxt(disk5_no_path, delimiter=",", skiprows=1)

disk7_no_path = parent_dir / "disk_7_nofloat.csv"
disk7_no = np.loadtxt(disk7_no_path, delimiter=",", skiprows=1)

nofloat = [disk4_no, disk5_no, disk7_no]
floating = [disk4_fl, disk5_fl, disk7_fl]


"""
theoretical line is given by ploting the following expression for Q(v):

\\xi \\sqrt(\\rho^2 Q^3 g/4 \\pi \\nu) == g (m_{disk} - \\rho V)+\\rho Q U

for derivation and physical meaning of symbols please refere to the manuscript
https://arxiv.org/abs/2312.13099
"""


def velocity(Q, m_disk, V):
    rho = 997
    nu = 10 ** (-6)
    g = 9.81
    xi = 0.441
    return (
        xi * (rho**2 * Q**3 * g / (4 * np.pi * nu)) ** (0.5) - g * (m_disk - rho * V)
    ) / (rho * Q)


yargs = np.linspace(30 * 10 ** (-6), 300 * 10 ** (-6), 100)

"""
Set of paramters for plots in form:
[radius in cm, mass of disk in g, uncertainty of mass in g, volume in ml, uncertainty of volume in ml]
"""

params = np.array(
    (
        [
            [4, 11.7, 0.1, 2.77, 0.05],
            [5, 30.7, 0.1, 14.92, 0.05],
            [7, 50.9, 0.2, 12.16, 0.05],
        ]
    )
)

step = 0
for pars in params:
    xargs = velocity(yargs, pars[1] * 10 ** (-3), pars[3] * 10 ** (-6))

    text = (
        r"Radius:\hspace{10pt}"
        + rf"$R = {pars[0]}$ cm"
        + "\n"
        + r"Mass:\hspace{20pt}"
        + rf"$m = \left({pars[1]} \pm {pars[2]}\right)$ g"
        + "\n"
        + r"Volume:\hspace{4pt}"
        + rf"$V = \left({pars[3]} \pm {pars[4]}\right)$ ml"
    )

    fontsize = 23

    plt.figure(figsize=(10, 5.5))
    plt.rcParams.update({"text.usetex": True, "font.family": "Cambria"})

    plt.errorbar(
        floating[step][:, 0],
        floating[step][:, 2],
        xerr=floating[step][:, 1],
        yerr=floating[step][:, 3],
        fmt="o",
        mfc="w",
        label=r"Disk floats",
    )
    plt.errorbar(
        nofloat[step][:, 0],
        nofloat[step][:, 2],
        xerr=nofloat[step][:, 1],
        yerr=nofloat[step][:, 3],
        fmt="o",
        color="#d39400",
        label=r"Disk sinks",
    )

    plt.plot(xargs, (10**6) * yargs, color="black", linestyle="--")

    if step < 2:
        plt.text(0.1, 170, text, fontsize=fontsize)
    else:
        plt.text(0.1, 20, text, fontsize=fontsize)

    plt.xlabel(r"Jet velocity $\left(U\right)$ [m/s]", fontsize=fontsize)
    plt.ylabel(r"Jet flow $\left(Q\right)$ [ml/s]", fontsize=fontsize)
    plt.xticks(fontsize=fontsize)
    plt.yticks(fontsize=fontsize)
    plt.legend(fontsize=fontsize, frameon=False, loc=4)

    plt.minorticks_on()
    plt.tick_params(which="both", top=True, right=True)

    plt.xlim(0, 3)
    plt.ylim(0, 230)

    plt.savefig(
        "graphs/float_nofloat_R" + str(int(pars[0])) + ".eps",
        format="eps",
        bbox_inches="tight",
    )
    step += 1
