import os
import plecsutil as pu
import matplotlib.pyplot as plt
plt.ion()

import model

# Plecs file
plecs_file = 'buck_intro'
plecs_file_path = os.path.abspath(os.getcwd())

# Plecs model
pm = pu.ui.PlecsModel(plecs_file, plecs_file_path, model.params())

# Runs simulation
R_vals = [2, 5, 10]
data = []
for r in R_vals:
    d = pm.sim(sim_params={'R': r})
    data.append(d)

# Plots results
plt.figure()
for d in data:
    label = 'R = {:}'.format(d.meta['model_params']['R'])
    plt.plot(d.t, d.data[:, 1], label=label)
plt.legend()
