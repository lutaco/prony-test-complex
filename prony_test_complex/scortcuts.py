import numpy as np
from pyrony.approximation import polynomial_method, matrix_pencil
from pyrony.prony_lowpass_filter import prony_restore_values
from scipy import signal as sc_signal


def mpm(signal, p, ts):
    params = matrix_pencil(signal, p, ts)
    return params, prony_restore_values(*params, len(signal), ts)


def classic(signal, p, ts):
    params = polynomial_method(signal, p, ts, 'classic')
    return params, prony_restore_values(*params, len(signal), ts)


def ls(signal, p, ts):
    params = polynomial_method(signal, p, ts, 'LS')
    return params, prony_restore_values(*params, len(signal), ts)


def tls(signal, p, ts):
    params = polynomial_method(signal, p, ts, 'TLS')
    return params, prony_restore_values(*params, len(signal), ts)


def empty_filter(data):
    sig = data['signal']
    return sig[:]


def win_filter(data):
    sig = data['signal']
    return sc_signal.wiener(sig)


def but_filter(data):
    sig = data['signal']
    ts = np.abs(data['range'][1] - data['range'][0]) / len(data['signal']) / (2 * np.pi)
    return sc_signal.filtfilt(*sc_signal.butter(3, data['ex_ts'], 'low', fs=1/ts), sig)
