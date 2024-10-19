import numpy as np
import scipy.signal

import plecsutil as pu

def params():

    V_in = 20
    Vo_ref = 10
    
    L = 47e-6
    RL = 20e-3
    
    C_out = 220e-6
    R_Cout = 50e-3
    
    f_pwm = 100e3

    R = 10
    Rd = 10

    params = {}
    params['L'] = L
    params['RL'] = RL
    
    params['C_out'] = C_out
    params['R_Cout'] = R_Cout

    params['R'] = R

    params['V_in'] = V_in
    params['Vo_ref'] = Vo_ref
    
    params['f_pwm'] = 100e3

    return params


