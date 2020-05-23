import math
import numpy as np
from scipy.linalg import toeplitz, hankel, pinv
from pyrony.regression_analysis import tls


def polynomial_method(x, p, Ts, method):

    N = len(x)

    if method == 'classic':
        if N != 2 * p:
            raise IOError('length x must be equals 2p in classic method')

    elif method not in ['LS', 'TLS', 'OLS']:
        raise IOError('error in parsing the argument methods')

    T = toeplitz(x[p-1:-1], np.flip(x[:p]))

    if method in ['classic', 'LS']:
        a = np.linalg.lstsq(-T, x[p:], rcond=None)[0]
    else:
        a = tls(T, -x[p:])

    if sum(np.isnan(a) | np.isinf(a)):
        raise IOError('not solution')

    c = np.hstack((1.0, *a.transpose()))
    r = np.roots(c)[np.newaxis].transpose()

    alfa = np.log(np.abs(r)) / Ts
    freq = np.arctan2(np.imag(r), np.real(r)) / (2 * math.pi * Ts)

    len_vandermonde = N if method in ['LS', 'TLS'] else p

    Z = np.power(np.tile(r, len_vandermonde).transpose(), np.array([range(len_vandermonde)]).transpose())

    if method in ['classic', 'LS']:
        h = np.linalg.lstsq(Z, x[:len_vandermonde], rcond=None)[0]
    else:
        indeterminate_form = np.sum(np.sum(np.isnan(Z) | np.isinf(Z)))

        if indeterminate_form:
            raise IOError("not indeterminate form")

        h = tls(Z, x[:len_vandermonde])

    Amp = np.abs(h)
    theta = np.arctan2(np.imag(h), np.real(h))

    return [Amp, alfa, freq, theta]


def matrix_pencil(x, p, Ts):

    N = len(x)
    Y = hankel(x[:-p], x[-p-1:])

    Y1 = Y[:, :-1]
    Y2 = Y[:, 1:]
    l = np.linalg.eig(pinv(Y1).dot(Y2))[0][np.newaxis].transpose()

    alfa = np.log(np.abs(l)) / Ts
    freq = np.arctan2(np.imag(l), np.real(l)) / (2 * np.pi * Ts)

    Z = np.power(np.tile(l, N).transpose(), np.array([range(N)]).transpose())

    h = np.linalg.lstsq(Z, x, rcond=None)[0]

    Amp = np.abs(h)
    theta = np.arctan2(np.imag(h), np.real(h))

    return [Amp, alfa, freq, theta]
