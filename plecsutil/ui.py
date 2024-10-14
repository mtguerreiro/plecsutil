"""
User interface
==============

"""
import plecsutil as pu

import numpy as np
import pickle
import zipfile


class Sim:

    def __init__(self, pfile, pfile_path, params_cb, ctl={}):

        self._pfile = pfile
        self._pfile_path = pfile_path
        
        self._params_cb = params_cb

        self._sim_data = {}
        

    def run(self, params={}, save=False):

        run_params = self._params_cb()

        for k, v in params.items():
            if k not in run_params:
                raise KeyError('Parameter \'{:}\' not a model parameter'.format(k))
            run_params[k] = v

        t, data = pu.pi.sim(self._pfile, self._pfile_path, run_params)

        while True:

            key = get_random_key()
            if key in self._sim_data:
                continue

            self._sim_data[key] = [t, data, run_params]
            break

        if save:
            save_data(save, [t, data, run_params])

        return key


    def get_sim_data(self, key):

        if key not in self._sim_data:
            raise KeyError('Invalid key.'.format(k))

        return (self._sim_data[key][0], self._sim_data[key][1], self._sim_data[key][2])


def get_random_key():

    return np.random.randint(2**32)


def load_data(path, file):

    with zipfile.ZipFile(path + file + '.zip', 'r') as zipf:
        data_bytes = zipf.read(file)

    data = pickle.loads(data_bytes)

    return data


def save_data(file, data):

    with zipfile.ZipFile(file + '.zip', 'w', compression=zipfile.ZIP_LZMA) as zipf:
        zipf.writestr(file, pickle.dumps(data))
