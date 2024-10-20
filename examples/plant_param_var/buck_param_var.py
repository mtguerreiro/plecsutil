import os
import plecsutil as pu

import numpy as np

import matplotlib
import matplotlib.pyplot as plt

import model

plt.ion()

# --- Input ---
plecs_file = 'buck_param_var'
plecs_file_path = os.path.abspath(os.getcwd())

sim_params = [
    {'RL': 0, 'R_Cout': 0},
    {'RL': 10e-3, 'R_Cout': 50e-3},
    ]

# --- Sim ---
# Plecs model
pm = pu.ui.PlecsModel(
    plecs_file, plecs_file_path,
    model.params,
    )

# Runs simulations
data = []
for sp in sim_params:
    d = pm.sim(sim_params=sp)
    data.append(d)

# --- Results ---
plt.figure()
xlim = [0, 20]

ax = plt.subplot(3,1,1)
plt.title('Duty-cycle')
for d in data:
    RL = d.meta['sim_params']['RL']
    R_Cout = d.meta['sim_params']['R_Cout']
    if np.allclose(RL, 0) and np.allclose(R_Cout, 0):
        label = 'Ideal'
    else:
        label = 'RL: {:}, R_Cout: {:}'.format(RL, R_Cout)
    plt.step(d.t / 1e-3, d.data[:, 2], where='post', label=label)
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
