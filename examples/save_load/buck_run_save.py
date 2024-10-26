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

# Run simulations and save data
ctl_params = [
    {'ts': 1e-3, 'os': 5},
    {'ts': 3e-3, 'os': 5},
    {'ts': 5e-3, 'os': 5}
    ]

files = ['sim_1', 'sim_2', 'sim_3']

data = []
for cp, f in zip(ctl_params, files):
    pm.sim(ctl_params=cp, save=f, ret_data=False)
