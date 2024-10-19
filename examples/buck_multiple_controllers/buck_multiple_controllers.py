import os
import plecsutil as pu

import numpy as np

import matplotlib
import matplotlib.pyplot as plt

import model

plt.ion()

# --- Input ---
pfile = 'buck_multiple_controllers'
pfile_path = os.path.abspath(os.getcwd())

ctl_params = [
    ['sfb', {'ts': 2e-3, 'os': 5}],
    ['casc', {'ts': 2e-3, 'os': 5}],
    ]

# --- Sim ---
# Sim object
sim = pu.ui.Sim(
    pfile, pfile_path,
    model.params,
    controllers=model.CONTROLLERS
    )

# Runs simulations (and saves data)
keys = []
for cp in ctl_params:
    key = sim.run(ctl=cp[0], ctl_params=cp[1], close_sim=False)
    keys.append(key)

# --- Results ---
data = []
for key in keys:
    data.append( sim.get_sim_data(key) )

# Plots the results
plt.figure()
xlim = [0, 20]

ax = plt.subplot(3,1,1)
plt.title('Duty-cycle')
for d in data:
    label = '{:}'.format( d.meta['ctl_label'] )
    plt.step(d.t / 1e-3, d.data[:, 3], where='post', label=label)
plt.grid()
plt.ylabel('$u$')
plt.legend()
plt.gca().tick_params(labelbottom=False)

plt.subplot(3,1,2, sharex=ax)
plt.title('Inductor current')
for d in data:
    plt.plot(d.t / 1e-3, d.data[:, 0])
plt.grid()
plt.ylabel('Current (A)')
plt.gca().tick_params(labelbottom=False)

plt.subplot(3,1,3, sharex=ax)
plt.title('Output voltage')
for d in data:
    plt.plot(d.t / 1e-3, d.data[:, 1])
plt.grid()
plt.ylabel('Voltage (V)')
plt.xlabel('Time (ms)')
plt.xlim(xlim)

plt.tight_layout()

