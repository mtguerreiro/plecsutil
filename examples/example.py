import os
import plecsutil as pu

import numpy as np

import matplotlib
import matplotlib.pyplot as plt

import model

plt.ion()

# --- Input ---

pfile = 'example'
pfile_path = os.path.abspath(os.getcwd())

sim = pu.ui.Sim(pfile, pfile_path, model.params)

sim_params = [
    {'a': 1},
    {'a': 10},
    {'a': 100}
    ]

keys = []

for sp in sim_params:
    fsave = '{:}_{:}'.format('a', sp['a'])
    key = sim.run(sp, save=fsave)
    keys.append(key)


for key in keys:
    t, data, params = sim.get_sim_data(key)
    plt.plot(t, data[:, 1], label='a = {:}'.format(params['a']))
    plt.legend()
