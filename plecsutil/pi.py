"""
Plecs interface
===============

"""
import numpy as np
import scipy.io
import io
import xmlrpc.client

def sim(file, file_path, sim_params={}, close=True):

    server = xmlrpc.client.Server("http://localhost:1080/RPC2")
    server.plecs.load(file_path + '/' + file)

    gen_m(file, file_path, sim_params)

    plecs_params = {'OutputFormat': 'MatFile'}
    data_raw = server.plecs.simulate(file, plecs_params).data
    data = scipy.io.loadmat(io.BytesIO(data_raw))

    t = data['Time'][0]
    sim_data = data['Values'].T

    if close is True:
        server.plecs.close(file)
    
    return t, sim_data


def gen_m(file, file_path, params):

    m_txt = ''

    for p, v in params.items():

        if type(v) is np.ndarray:
            v = np.array2string(v, separator=',', floatmode='unique').replace('\n', '')

        m_txt += '{:} = {:};\n'.format(p, v)

    with open(file_path + '/' + file + '.m', 'w') as f:
        f.write(m_txt)
