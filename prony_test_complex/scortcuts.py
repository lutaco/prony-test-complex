from pyprony.approximation import polynomial_method, matrix_pencil
from pyprony.prony_lowpass_filter import prony_restore_values, quick_prony_restore_values
from scipy import signal as sc_signal


def mpm(signal, p, ts):
    params = matrix_pencil(signal, p, ts)
    return params, prony_restore_values(*params, len(signal), ts)


def ls(signal, p, ts):
    params = polynomial_method(signal, p, ts, 'LS')
    return params, prony_restore_values(*params, len(signal), ts)


def s_ls(signal, p, ts):
    params = polynomial_method(signal, p, ts, 'LS')
    return params, quick_prony_restore_values


def s_mpm(signal, p, ts):
    params = matrix_pencil(signal, p, ts)
    return params, quick_prony_restore_values


def empty_filter(data):
    sig = data['signal']
    return sig[:]


def win_filter(data):
    sig = data['signal']
    return sc_signal.wiener(sig)


def but_filter(data):
    sig = data['signal']
    return sc_signal.filtfilt(*sc_signal.butter(5, data['ex_fs'], 'low', fs=data['fs']), sig)


def s_but_filter(data):
    sig = data['signal']
    return sc_signal.filtfilt(*sc_signal.butter(5, data['ex_fs'], 'low', fs=data['new_fs']), sig)
