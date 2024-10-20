import os
import plecsutil as pu
import matplotlib.pyplot as plt
plt.ion()

# Model params
model_params = {
    'f_pwm': 100e3,
    'V_in': 24,
    'R': 10,
    'L': 47e-6,
    'C': 220e-6
    }

# Plecs file
plecs_file = 'buck_intro'
plecs_file_path = os.path.abspath(os.getcwd())

# Plecs model
pm = pu.ui.PlecsModel(plecs_file, plecs_file_path, model_params)

# Runs simulation
data = pm.sim()

# Plots results
plt.figure()
plt.plot(data.t, data.data[:, 1])
