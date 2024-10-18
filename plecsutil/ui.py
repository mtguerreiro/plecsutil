"""
User interface
==============

"""
import plecsutil as pu

import numpy as np

from dataclasses import dataclass
import pickle
import zipfile


@dataclass
class Controller:
    ctl_id : int
    get_gains: callable


@dataclass
class DataSet:
    t : np.ndarray
    data : np.ndarray
    source : str
    meta : {}


class Sim:

    def __init__(self, pfile, pfile_path, params_cb, controllers=None):

        self._pfile = pfile
        self._pfile_path = pfile_path
        
        self._params_cb = params_cb

        self._sim_data = {}

        self._controllers = controllers


    def run(self, sim_params={}, ctl=None, ctl_params={}, keep=True, save=False, close_sim=True):

        model_params = self._params_cb()

        # Updates model params with sim params
        for k, v in sim_params.items():
            if k not in model_params:
                raise KeyError('Parameter \'{:}\' not a model parameter'.format(k))
            model_params[k] = v

        # Updates model params with ctl params
        if ctl:
            n_ctl = len(self._controllers)
            active_ctl = self._controllers[ctl].id
            c_params = gen_controllers_params(n_ctl, active_ctl)

            ctl_gains = self._controllers[ctl].get_gains(ctl_params)
            c_params.update( ctl_gains )
            
            for k, v in c_params.items():
                if k not in model_params:
                    raise KeyError('Parameter \'{:}\' not a model parameter'.format(k))
                model_params[k] = v

        t, data, plecs_header = pu.pi.sim(self._pfile, self._pfile_path, model_params, close=close_sim)

        meta = {'sim_params': model_params, 'ctl_params': ctl_params}
        sim_data = DataSet(t, data, plecs_header, meta)
        
        if keep is True:
            key = self.get_random_key()
            self._sim_data[key] = sim_data    
         
        if save:
            save_data(save, sim_data)
            
        return key


    def get_sim_data(self, key):

        if key not in self._sim_data:
            raise KeyError('Invalid key.')

        return self._sim_data[key]


    def get_random_key(self):

        while True:
            key = np.random.randint(2**31)
            if key in self._sim_data:
                continue
            break
            
        return key


def gen_controllers_params(n_ctl, active_ctl):

    ctls_params = {
        'N_CTL': n_ctl,
        'CTL_SEL': active_ctl,
        'CTL_EN': 'zeros(1, N_CTL)',
        'CTL_EN(CTL_SEL)': 1
        }

    return ctls_params


def load_data(file):

    with zipfile.ZipFile(file + '.zip', 'r') as zipf:
        data_bytes = zipf.read('DataSet')

    data = pickle.loads(data_bytes)

    return data


def save_data(file, data):

    with zipfile.ZipFile(file + '.zip', 'w', compression=zipfile.ZIP_LZMA) as zipf:
        zipf.writestr('DataSet', pickle.dumps(data))
