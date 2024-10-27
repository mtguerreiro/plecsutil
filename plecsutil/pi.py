import numpy as np
import scipy.io
import io
import xmlrpc.client

def sim(file, file_path, sim_params, close=True):
    """Simulates a PLECS model.

    Before running the simulation, ``sim_params`` is used to create a ``.m``
    file containing the parameters of the model.

    Parameters
    ----------
    file : str
        The filename of the model (without path and the ``.plecs`` extension).
    
    file_path : str
        The path to the directory containing the model file.

    sim_params : dict
        A dictionary with the model parameters for the simulation. This
        dictionary must contain all parameters required by the model. The
        dictionary should contain only float, int or numpy arrays as values.
    
    close : bool, optional
        Whether to close PLECS after running the simulation. Default is `True`.

    Returns
    -------
    tuple
        A tuple containing:
            - t (N-size numpy.ndarray): Simulation time vector.
            - sim_data ((N, M) numpy.ndarray): Array of simulation data values.
            - plecs_header (str): Header information from the PLECS output file.
    
    """
    server = xmlrpc.client.Server("http://localhost:1080/RPC2")
    server.plecs.load(file_path + '/' + file)

    gen_m(file, file_path, sim_params)

    plecs_params = {'OutputFormat': 'MatFile'}
    data_raw = server.plecs.simulate(file, plecs_params).data
    data = scipy.io.loadmat(io.BytesIO(data_raw))

    t = data['Time'][0]
    sim_data = data['Values'].T

    plecs_header = data['__header__']

    if close is True:
        server.plecs.close(file)
    
    return (t, sim_data, plecs_header)


def gen_m(file, file_path, params):
    """
    Generates the ``.m`` file containing all model parameters required for the
    simulation.

    Parameters
    ----------
    file : str
        Name of the PLECS model file (without path and `.plecs` extension).
        The ``.m`` file is created with the same name as the PLECS model.

    file_path : str
        Path to the directory where the ``.m`` file will be saved.

    sim_params : dict
        Dictionary with model parameters for the simulation. 

    """
    m_txt = ''

    for p, v in params.items():

        if type(v) is np.ndarray:
            v = _format_np_array_string(v)

        m_txt += '{:} = {:};\n'.format(p, v)

    with open(file_path + '/' + file + '.m', 'w') as f:
        f.write(m_txt)


def _format_np_array_string(arr):

    arr_txt = np.array2string(arr, separator=',', floatmode='unique')
    arr_txt = arr_txt.replace('\n', '')
    arr_txt = arr_txt.replace('],', '];')

    return arr_txt    
