import plecsutil as pu

import matplotlib.pyplot as plt
plt.ion()

# --- Input ---
files = ['sim_1', 'sim_2', 'sim_3']

# --- Loads results ---
data = []
for f in files:
    data.append( pu.ui.load_data(f) )

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
