import numpy as np
import scipy.signal

def plant_params():

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


def controller_gains(ctl_params):
    
    ts = ctl_params['ts']
    os = ctl_params['os']

    _plant_params = plant_params()
    R = _plant_params['R']
    L = _plant_params['L']
    C = _plant_params['C_out']
    V_in = _plant_params['V_in']
    
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


def params():

    # Plant parameters
    _plant_params = plant_params()

    # Control parameters
    ts = 2e-3
    os = 5
    _ctl_params = controller_gains({'ts':ts, 'os':os})

    # Model params
    _params = {}
    _params.update( _plant_params )
    _params.update( _ctl_params )
    
    return _params
