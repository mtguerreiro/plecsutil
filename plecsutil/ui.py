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
    """Data generated from a PLECS simulation."""

    #: N-size vector with time steps of the simulation
    t : np.ndarray

    #: (N, M) matrix containing the signals connected to the output data ports
    data : np.ndarray

    #: PLECS info (version, time and date of simulation)
    source : str

    #: A dictionary containing model and controller paramaters used to run the simulation.
    meta : {}


class PlecsModel:

    def __init__(self, file, file_path, model_params, get_ctl_gains=None, controllers=None):

        self._file = file
        self._file_path = file_path
        
        self._model_params = dict(model_params)

        self._sim_data = {}

        self._get_ctl_gains = get_ctl_gains
        self._controllers = controllers


    def sim(self, sim_params={}, ctl=None, ctl_params={}, ret_data=True, save=False, close_sim=True):

        model_ctl_params, ctl_label = self._get_model_ctl_params(ctl, ctl_params)

        # Creats a user_params dict with new sim and ctl params        
        user_params = {}
        user_params.update(sim_params)
        user_params.update(model_ctl_params)

        # Updates model_params with user params
        model_params = dict(self._model_params)
        for k, v in user_params.items():
            if k not in model_params:
                raise KeyError('Parameter \'{:}\' not a model parameter'.format(k))
            model_params[k] = v

        # Runs simulation with new model_params
        t, data, plecs_header = pu.pi.sim(self._file, self._file_path, model_params, close=close_sim)

        meta = {'model_params': model_params}
        if ctl_params:
            meta.update( {'ctl_params': ctl_params} )
        if ctl is not None:
            meta.update( {'ctl': ctl, 'ctl_label': ctl_label} )
        
        sim_data = DataSet(t, data, plecs_header, meta)

        if save:
            save_data(save, sim_data)
        
        if ret_data is True:
            return sim_data


    def _get_model_ctl_params(self, ctl, ctl_params):

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
            if type(self._controllers) is Controller:
                model_ctl_params.update( self._controllers.get_gains(ctl_params) )
            else:
                model_ctl_params.update( self._get_ctl_gains(ctl_params) )

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
