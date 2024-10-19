import numpy as np
import scipy.signal

import plecsutil as pu

def params():

    # Plant parameters
    plant_params = get_plant_params()

    # Control parameters
    ts = 2e-3
    os = 5

    sfb_params = sfb_get_gains({'ts':ts, 'os':os})
    casc_params = cascaded_get_gains({'ts':ts, 'os':os})

    ctl_params = {}
    ctl_params.update(sfb_params)
    ctl_params.update(casc_params)

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

    zeta, wn = _zeta_wn(ts, os)

    p1 = - zeta * wn + 1j * wn * np.sqrt(1 - zeta**2)
    p2 = np.conj(p1)
    p3 = 5 * p1.real
    
    K = scipy.signal.place_poles(Aa, Ba, (p1, p2, p3)).gain_matrix

    Kx = K[0, :2]
    Ke = K[0, 2]
    
    return {'Kx': Kx, 'Ke': Ke}


def cascaded_get_gains(ctl_params):

    sys_params = get_plant_params()
    R = sys_params['R']
    L = sys_params['L']
    C = sys_params['C_out']
    V_in = sys_params['V_in']

    ts_v = ctl_params['ts']
    os_v = ctl_params['os']
    
    os_i = os_v
    ts_i = ts_v / 5

    zeta_i, wn_i = _zeta_wn(ts_i, os_i)
    ki = (L / V_in) * 2 * zeta_i * wn_i
    k_ei = (L / V_in) * ( - wn_i**2 )

    zeta_v, wn_v = _zeta_wn(ts_v, os_v)
    kv = ( C ) * ( 2 * zeta_v * wn_v - 1 / R / C )
    k_ev = ( C ) * ( - wn_v**2 )

    params = {'ki': ki, 'k_ei': k_ei, 'kv': kv, 'k_ev':k_ev}

    return params


def _zeta_wn(ts, os):

    zeta = -np.log(os / 100) / np.sqrt( np.pi**2 + np.log(os / 100)**2 )
    wn = 4 / ts / zeta

    return (zeta, wn)


CONTROLLERS = {
    'sfb':  pu.ui.Controller(1, sfb_get_gains),
    'cascaded': pu.ui.Controller(2, cascaded_get_gains)
}


