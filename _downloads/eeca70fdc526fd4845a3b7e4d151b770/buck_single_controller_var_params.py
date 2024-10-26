import os

import plecsutil as pu
import model

import matplotlib.pyplot as plt
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

# Runs simulations
data = []
ctl_params = [
    {'ts': 1e-3, 'os': 5},
    {'ts': 3e-3, 'os': 5},
    {'ts': 5e-3, 'os': 5}
    ]
for cp in ctl_params:
    d = pm.sim(ctl_params=cp, close_sim=False)
    data.append(d)

# --- Results ---
plt.figure()
xlim = [0, 20]

ax = plt.subplot(3,1,1)
plt.title('Duty-cycle')
for d in data:
    label = '$T_s = {:}$ ms'.format( d.meta['ctl_params']['ts'] / 1e-3 )
    plt.step(d.t / 1e-3, d.data[:, 3], label=label, where='post')
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
