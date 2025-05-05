import plecsutil as pu

import numpy as np

from dataclasses import dataclass
import pickle
import zipfile


@dataclass
class Controller:
    """A class to represent multiple controllers in a PLECS model."""

    #: Port of the multiport switch that the controller is connected to.
    port : int = 1

    #: Callback to get the gains of the controller that are used in the model.
    #: The function should take a dictionary with the controller parameters as
    #: argument, and return a dictionary with the model parameters.
    get_gains : callable = None

    #: A label for the controller. 
    label : str = ''


@dataclass
class DataSet:
    """A dataclass to hold data generated from a PLECS simulation."""

    #: N-size vector with time steps of the simulation.
    t : np.ndarray

    #: (N, M) matrix containing the signals connected to the output data ports.
    data : np.ndarray

    #: PLECS info (version, time and date of simulation).
    source : str

    #: A dictionary containing model and controller paramaters used to run the
    #: simulation. The dictionary always contain the following key:
    #:
    #: * ``model_params``: The dictionary with the model parameters used in the
    #:   simulation.
    #:
    #: The dictionary may contain the following keys, if they are specified
    #: when running a simulation:
    #:
    #: * ``ctl``: Controller used in the simulation. Only for models with
    #:   multiple controllers.  
    #: * ``ctl_params``: Parameters used to generate the gains/parameters of the
    #:   controller.
    #: * ``ctl_label``: :attr:`Controller.label` of controller used for the
    #:   simulation.
    #: * ``extras``: Extra metadata that might be useful storing. 
    meta : {}


class PlecsModel:
    """A class representing a PLECS  model.

    :class:`PlecsModel` provides a framework to set up and run simulations,
    and manage parameters of the model and its controllers.

    Parameters
    ----------
    file : str
        The filename of the model (without the ``.plecs`` extension).
    
    file_path : str
        The path to the directory containing the model file.

    model_params : dict
        A dictionary of model parameters for the simulation. These parameters 
        are used to initialize the model and can be overridden by
        simulation-specific parameters when running simulations.

    get_ctl_gains : callable, optional
        A function for retrieving control gains for the model's controller.
        Only relevant if the model has a single controller.

    controllers : :class:`Controller`, optional
        An object representingthe  controllers of the model. Only relevant for
        models with multiple controllers.
    
    """
    def __init__(self, file, file_path, model_params, get_ctl_gains=None, controllers=None):

        self._file = file
        self._file_path = file_path
        
        self._model_params = dict(model_params)

        self._sim_data = {}

        self._get_ctl_gains = get_ctl_gains
        self._controllers = controllers


    def sim(self, sim_params={}, ctl=None, ctl_params={}, extra_meta={}, ret_data=True, save=False, close_sim=True):
        """Runs the PLECS simulation with specified parameters and returns the
        simulation data.

        Parameters
        ----------
        sim_params : dict, optional
            Dictionary of simulation parameters to override the model's default
            parameters. If not set, the simulation is executed with the default
            parameters.

        ctl : NoneType or str, optional
            Sets the controller to be enabled in the simulation, in case of
            models with multiple controllers. If not set, the simulation runs
            with the default controller and its parameters (if there are any).

        ctl_params : dict, optional
            Controller parameters, in case of model with one or more
            controllers. If not set, the default controller parameters are used
            for the simulation (if there is one).

        extra_meta : dict, optional
            Extra metadata used to build the controller or run the simulation
            that don't fit in the other meta fields.

        ret_data : bool, optional
            Whether to return the simulation. Default is `True`.

        save : bool or str, optional
            Specifies whether to save the simulation data. If `False`, the data
            is not saved. If a string is provided, it will be used as the
            filename to save the data. Default is `False`.

        close_sim : bool, optional
            Whether to close PLECS after running the simulation. Default is
            `True`.

        Returns
        -------
        :class:`DataSet`
            A :class:`DataSet` object containing the simulation data. Returned
            only if `ret_data` is set to `True`.

        Raises
        ------
        KeyError
            If any parameter in ``sim_params`` or ``ctl_params`` does not exist
            in the default model parameters, ``KeyError`` is raised.

        """
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
        if extra_meta:
            meta.update( {'extras': extra_meta} )
        
        sim_data = DataSet(t, data, plecs_header, meta)

        if save:
            save_data(save, sim_data)
        
        if ret_data is True:
            return sim_data


    def gen_m_file(self, sim_params={}, ctl=None, ctl_params={}):
        """Generates the `.m` file for the simulation model.

        Parameters
        ----------
        sim_params : dict, optional
            Dictionary of simulation parameters to override the model's default
            parameters. If not set, the simulation is executed with the default
            parameters.

        ctl : NoneType or str, optional
            Sets the controller to be enabled in the simulation, in case of
            models with multiple controllers. If not set, the simulation runs
            with the default controller and its parameters (if there are any).

        ctl_params : dict, optional
            Controller parameters, in case of model with one or more
            controllers. If not set, the default controller parameters are used
            for the simulation (if there is one).

        Raises
        ------
        KeyError
            If any parameter in ``sim_params`` or ``ctl_params`` does not exist
            in the default model parameters, ``KeyError`` is raised.

        """
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

        # Generates .m file
        pu.pi.gen_m(self._file, self._file_path, model_params)

        
    def _get_model_ctl_params(self, ctl, ctl_params):

        model_ctl_params = {}
        ctl_label = None
        
        if ctl:
            n_ctl = len(self._controllers)
            active_ctl = self._controllers[ctl].port
            c_params = gen_controllers_params(n_ctl, active_ctl)
            model_ctl_params.update( c_params )

            ctl_gains = self._controllers[ctl].get_gains(ctl_params)
            model_ctl_params.update( ctl_gains )
            ctl_label = self._controllers[ctl].label
            
        else:
            if type(self._controllers) is Controller:
                model_ctl_params.update( self._controllers.get_gains(ctl_params) )
            else:
                if self._get_ctl_gains is not None:
                    model_ctl_params.update( self._get_ctl_gains(ctl_params) )

        return model_ctl_params, ctl_label


def gen_controllers_params(n_ctl, active_ctl):
    """
    Generates the logic to set controllers in models with multiple controllers.

    Parameters
    ----------
    n_ctl : int
        The total number of controllers.

    active_ctl : int
        The index of the active controller to be enabled in the simulation.

    Returns
    -------
    dict
        Logic for the ``.m`` file as a dictionary.

    """
    ctls_params = {
        'N_CTL': n_ctl,
        'CTL_SEL': active_ctl,
        'CTL_EN': 'zeros(1, N_CTL)',
        'CTL_EN(CTL_SEL)': 1
        }

    return ctls_params


def load_data(file):
    """Loads simulation data from a zipped file.

    Parameters
    ----------
    file : str
        Name of the file, without ``.zip``. Must include the full or relative
        path if ``file`` is in a different directory.

    Returns
    -------
    data : :class:`DataSet`
        Data loaded from the specified file.

    """
    with zipfile.ZipFile(file + '.zip', 'r') as zipf:
        data_bytes = zipf.read('DataSet')

    data = pickle.loads(data_bytes)

    return data


def save_data(file, data):
    """Saves simulation data to a zipped file.

    Parameters
    ----------
    file : str
        Name of the file (without the ``.zip`` extension). The name can contain
        a relative or full path.

    data : :class:`DataSet`
        Simulation data.

    """
    with zipfile.ZipFile(file + '.zip', 'w', compression=zipfile.ZIP_LZMA) as zipf:
        zipf.writestr('DataSet', pickle.dumps(data))
