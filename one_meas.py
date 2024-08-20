import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
# from scipy.optimize import minimize 

parent_dir = Path(__file__).parent

# import data
typeiia_path = parent_dir / "single_meas/type_iia.csv"
typeiia = np.loadtxt(typeiia_path, delimiter=",", skiprows=1)

typei_path = parent_dir / "single_meas/type_i.csv"
typei = np.loadtxt(typei_path, delimiter=",", skiprows=1)


fontsize = 23

plt.figure(figsize=(10, 5.5))
plt.rcParams.update({"text.usetex": True, "font.family": "Cambria"})

plt.errorbar(typeiia[:,0], typeiia[:,2], xerr=typeiia[:,1], fmt='o', label=r"Depth of type IIa")
plt.errorbar(typei[:,0], typei[:,2], xerr=typei[:,1], fmt='s', color='#d39400', label=r"Depth of type I")


plt.xlabel(r"Flow $\left(Q\right)$ [ml/s]", fontsize=fontsize)
plt.ylabel(r"Transition height $\left(H\right)$ [mm]", fontsize=fontsize)
plt.xticks(fontsize=fontsize)
plt.yticks(fontsize=fontsize)
plt.legend(fontsize=fontsize, frameon=False)

plt.minorticks_on()
plt.tick_params(which = 'both',top=True, right=True )

plt.xlim(0, 139)
plt.ylim(0, 6.9)

plt.savefig("graphs/plot_up_low.eps",format='eps',bbox_inches='tight')
plt.show()