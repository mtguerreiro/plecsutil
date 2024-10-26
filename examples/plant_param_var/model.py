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

    _params = {}
    _params['L'] = L
    _params['RL'] = RL
    
    _params['C_out'] = C_out
    _params['R_Cout'] = R_Cout

    _params['R'] = R

    _params['V_in'] = V_in
    _params['Vo_ref'] = Vo_ref
    
    _params['f_pwm'] = 100e3

    return _params


