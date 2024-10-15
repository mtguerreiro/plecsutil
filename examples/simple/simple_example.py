import os
import plecsutil as pu

import numpy as np

import matplotlib
import matplotlib.pyplot as plt

import model

plt.ion()

# --- Input ---
pfile = 'simple_example'
pfile_path = os.path.abspath(os.getcwd())

# --- Sim ---
# Sim object
sim = pu.ui.Sim(pfile, pfile_path, model.params)

# Sim params
sim_params = [
    {'zeta': 0.6},
    {'zeta': 0.7},
    {'zeta': 0.8}
    ]

# Runs simulations (and saves data)
keys = []
for sp in sim_params:
    fsave = '{:}_{:}'.format('zeta', sp['zeta'])
    key = sim.run(sp, save=fsave)
    keys.append(key)

# --- Results ---
# Plots the results
for key in keys:
    data = sim.get_sim_data(key)
    label = 'zeta = {:}'.format(data.meta['sim_params']['zeta'])
    plt.plot(data.t, data.data[:, 1], label=label)
    plt.legend()
