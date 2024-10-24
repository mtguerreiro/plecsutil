import os
import plecsutil as pu

import numpy as np

import matplotlib
import matplotlib.pyplot as plt

import model

plt.ion()

# --- Input ---
plecs_file = 'buck_multiple_controllers'
plecs_file_path = os.path.abspath(os.getcwd())

# --- Sim ---
# Plecs model
pm = pu.ui.PlecsModel(
    plecs_file, plecs_file_path,
    model.params(),
    controllers=model.CONTROLLERS
    )

# Runs simulations
d1 = pm.sim(ctl='sfb', ctl_params={'ts':1.5e-3, 'os':5})
d2 = pm.sim(ctl='casc', ctl_params={'ts_v':1.5e-3, 'os_v':5, 'ts_i':0.15e-3, 'os_i':5})
data  = [d1, d2]

# --- Results ---
plt.figure()
xlim = [0, 20]

ax = plt.subplot(2,1,1)
plt.title('Duty-cycle')
for d in data:
    label = '{:}'.format( d.meta['ctl_label'] )
    plt.step(d.t / 1e-3, d.data[:, 3], where='post', label=label)
plt.grid()
plt.ylabel('$u$')
plt.legend()
plt.gca().tick_params(labelbottom=False)

plt.subplot(2,1,2, sharex=ax)
plt.title('Output voltage')
for d in data:
    plt.plot(d.t / 1e-3, d.data[:, 1])
plt.grid()
plt.ylabel('Voltage (V)')
plt.xlabel('Time (ms)')
plt.xlim(xlim)

plt.tight_layout()
