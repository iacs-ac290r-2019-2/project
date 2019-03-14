# The script vetsion of Schlierin_vizualization.py

import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
import dask

import sys

k_str = sys.argv[1]
k = float(k_str)
print("K for Schlierin: ", k)

dir_name = './movie_schlieren_k{0}/'.format(k_str)
print("directory name: ", dir_name)

dr = xr.open_dataarray('./temperature_512core_processed.nc', chunks={'time': 15})

grad_T = np.sqrt(dr.differentiate('x')**2 + dr.differentiate('y')**2)
max_grad_T = 310.859439  # do not recompute

sch = np.exp(-k*grad_T/max_grad_T) # schlieren
sch = sch.rename('schlieren')

plt.rcParams['xtick.labelsize'] = 13
plt.rcParams['ytick.labelsize'] = 13
plt.rcParams['axes.titlesize'] = 20
plt.rcParams['axes.labelsize'] = 15

for t in range(0, 225):
    print(t, end=' ')
    fig, ax = plt.subplots(1, 1, figsize=[14, 5])
    sch[t].plot(ax=ax, vmin=0, vmax=1, cmap='Greys', extend='both')
    ax.set_title('Schlierin; time={0:.4f} s'.format(dr['time'][t].values), fontsize=15)
    fig.savefig(dir_name+'frame_{0:03d}.png'.format(t), dpi=300)
    plt.close()