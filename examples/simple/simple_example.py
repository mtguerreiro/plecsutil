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
data = []
for sp in sim_params:
    fsave = '{:}_{:}'.format('zeta', sp['zeta'])
    d = sim.run(sim_params=sp, save=fsave)
    data.append(d)

# --- Results ---
# Plots the results
for d in data:
    label = 'zeta = {:}'.format(d.meta['sim_params']['zeta'])
    plt.plot(d.t, d.data[:, 1], label=label)
    plt.legend()
