import numpy as np
import scipy.signal

import plecsutil as pu

def params():

    # Plant parameters
    plant_params = get_plant_params()

    # Control parameters
    ts = 2e-3
    os = 5
    ctl_params = sfb_get_gains({'ts':ts, 'os':os})

    # Params for plecs
    params = {}
   
    for k, v in plant_params.items():
        params[k] = v
    
    for k, v in ctl_params.items():
        params[k] = v
    
    return params


def get_plant_params():

    V_in = 20
    Vo_ref = 10

    L = 47e-6
    C_out = 220e-6

    f_pwm = 100e3

    R = 10
    Rd = 10

    params = {}
    params['L'] = L
    params['C_out'] = C_out
    params['R'] = R
    params['Rd'] = Rd

    params['V_in'] = V_in
    params['Vo_ref'] = Vo_ref
    
    params['f_pwm'] = 100e3

    return params


def sfb_get_gains(ctl_params):
    
    ts = ctl_params['ts']
    os = ctl_params['os']

    sys_params = get_plant_params()
    R = sys_params['R']
    L = sys_params['L']
    C = sys_params['C_out']
    V_in = sys_params['V_in']
    
    A = np.array([
        [0,       -1 / L],
        [1 / C,   -1 / R / C]
        ])
    
    B = np.array([
        [V_in / L],
        [0]
        ])

    C = np.array([0, 1])
    
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


CONTROLLERS = pu.ui.Controller(get_gains=sfb_get_gains)

