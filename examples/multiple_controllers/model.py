import numpy as np
import scipy.signal

from dataclasses import dataclass

import plecsutil as pu

    
def params():

    # Plant parameters
    plant_params = get_plant_params()

    # Control parameters
    ts = 2e-3
    os = 5
    ctl_params = sfb_get_gains({'ts':ts, 'os':os})

    # List of controllers
    n_ctl = len(CONTROLLERS)
    active_ctl = 0
    l_ctl = pu.ui.gen_controllers_params(n_ctl, active_ctl)

    # Params for plecs
    params = {}
    params.update(plant_params)
    params.update(ctl_params)
    params.update(l_ctl)
    
    return params


def get_plant_params():

    L = 47e-6
    C = 220e-6

    R = 10

    V_in = 24

    A = np.array([
        [0, -1 / L],
        [1 / C, - 1 / R / C]
        ])

    B = np.array([
        [V_in / L],
        [0]
        ])

    C = np.array([0, 1])

    return {'A':A, 'B':B, 'C':C}


def sfb_get_gains(ctl_params):
    
    ts = ctl_params['ts']
    os = ctl_params['os']

    sys_params = get_plant_params()
    A = sys_params['A']
    B = sys_params['B']
    C = sys_params['C']

    Aa = np.zeros((3,3))
    Aa[:2, :2] = A
    Aa[2, :2] = -C

    Ba = np.zeros((3, 1))
    Ba[:2, 0] = B[:, 0]

    zeta = -np.log(os / 100) / np.sqrt( np.pi**2 + np.log(os / 100)**2 )
    wn = 4 / ts / zeta

    p1 = - zeta * wn + 1j * wn * np.sqrt(1 - zeta**2)
    p2 = np.conj(p1)
    p3 = 5 * p1.real
    
    K = scipy.signal.place_poles(Aa, Ba, (p1, p2, p3)).gain_matrix

    Kx = K[0, :2]
    Ke = K[0, 2]
    
    return {'Kx': Kx, 'Ke': Ke}


CONTROLLERS = {
    'sfb': pu.ui.Controller(0, sfb_get_gains)
}
