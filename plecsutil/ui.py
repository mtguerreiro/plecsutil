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
    ctl_id : int = 1
    get_gains : callable = None
    label : str = ''


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


    def run(self, sim_params={}, ctl=None, ctl_params={}, ret_data=True, save=False, close_sim=True):

        model_params = self._params_cb()
        model_ctl_params, ctl_label = self.get_model_ctl_params(ctl, ctl_params)
        
        user_params = {}
        user_params.update(sim_params)
        user_params.update(model_ctl_params)

        # Updates model params with user params (sim + ctl)
        for k, v in user_params.items():
            if k not in model_params:
                raise KeyError('Parameter \'{:}\' not a model parameter'.format(k))
            model_params[k] = v

        t, data, plecs_header = pu.pi.sim(self._pfile, self._pfile_path, model_params, close=close_sim)

        meta = {'sim_params': model_params, 'ctl_params': ctl_params}
        if ctl is not None:
            meta.update( {'ctl': ctl, 'ctl_label': ctl_label} )
        
        sim_data = DataSet(t, data, plecs_header, meta)

        if save:
            save_data(save, sim_data)
        
        if ret_data is True:
            return sim_data


    def get_model_ctl_params(self, ctl, ctl_params):

        model_ctl_params = {}
        ctl_label = None
        
        if ctl:
            n_ctl = len(self._controllers)
            active_ctl = self._controllers[ctl].ctl_id
            c_params = gen_controllers_params(n_ctl, active_ctl)
            model_ctl_params.update( c_params )

            ctl_gains = self._controllers[ctl].get_gains(ctl_params)
            model_ctl_params.update( ctl_gains )
            ctl_label = self._controllers[ctl].label
        elif ctl_params:
            model_ctl_params.update( self._controllers.get_gains(ctl_params) )

        return model_ctl_params, ctl_label


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
