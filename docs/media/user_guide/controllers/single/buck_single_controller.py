import os
import plecsutil as pu

import numpy as np

import matplotlib
import matplotlib.pyplot as plt

import model

plt.ion()

# --- Input ---
plecs_file = 'buck_single_controller'
plecs_file_path = os.path.abspath(os.getcwd())

# --- Sim ---
# Plecs model
pm = pu.ui.PlecsModel(
    plecs_file, plecs_file_path,
    model.params(),
    get_ctl_gains=model.controller_gains
    )

# Runs simulation
data = pm.sim(ctl_params={'ts': 2.5e-3, 'os': 5})

# --- Results ---
plt.figure()
xlim = [0, 20]

ax = plt.subplot(2,1,1)
plt.title('Duty-cycle')
plt.step(data.t / 1e-3, data.data[:, 3], where='post')
plt.grid()
plt.ylabel('$u$')
plt.gca().tick_params(labelbottom=False)

plt.subplot(2,1,2, sharex=ax)
plt.title('Output voltage')
plt.plot(data.t / 1e-3, data.data[:, 1])
plt.grid()
plt.ylabel('Voltage (V)')
plt.xlabel('Time (ms)')
plt.xlim(xlim)

plt.tight_layout()
