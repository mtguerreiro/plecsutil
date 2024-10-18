import os
import plecsutil as pu

import numpy as np

import matplotlib
import matplotlib.pyplot as plt

import model

plt.ion()

### --- Input ---
##pfile = 'multiple_controllers'
##pfile_path = os.path.abspath(os.getcwd())
##
##ctl_params = [
##    {'ts': 1e-3, 'os': 5},
##    {'ts': 5e-3, 'os': 5},
##    {'ts': 10e-3, 'os': 5}
##    ]
##
### --- Sim ---
### Sim object
##sim = pu.ui.Sim(
##    pfile, pfile_path,
##    model.params,
##    ctl_params_cb=model.get_controller_gains
##    )
##
### Runs simulations (and saves data)
##keys = []
##for cp in ctl_params:
##    key = sim.run(ctl_params=cp, close_sim=False)
##    keys.append(key)
##
### --- Results ---
##data = []
##for key in keys:
##    data.append( sim.get_sim_data(key) )
##
### Plots the results
##plt.figure()
##xlim = [0, 10]
##
##ax = plt.subplot(3,1,1)
##for d in data:
##    label = '$T_s = {:}$ ms'.format( d.meta['ctl_params']['ts'] / 1e-3 )
##    plt.plot(d.t / 1e-3, d.data[:, 2], label=label)
##plt.grid()
##plt.ylabel('$u$')
##plt.legend()
##plt.gca().tick_params(labelbottom=False)
##
##plt.subplot(3,1,2, sharex=ax)
##for d in data:
##    plt.plot(d.t / 1e-3, d.data[:, 0])
##plt.grid()
##plt.ylabel('$x_1$')
##plt.gca().tick_params(labelbottom=False)
##
##plt.subplot(3,1,3, sharex=ax)
##for d in data:
##    plt.plot(d.t / 1e-3, d.data[:, 1])
##plt.grid()
##plt.ylabel('$x_2$')
##plt.xlabel('Time (ms)')
##plt.xlim(xlim)
##
##plt.tight_layout()
