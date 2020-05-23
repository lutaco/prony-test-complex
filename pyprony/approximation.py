import math
import numpy as np
from scipy.linalg import toeplitz, hankel, pinv
from pyprony.regression_analysis import tls


def polynomial_method(x, p, ts, method):

    size = len(x)

    if method == 'classic':
        if size != 2 * p:
            raise IOError('length x must be equals 2p in classic method')

    elif method not in ['LS', 'TLS', 'OLS']:
        raise IOError('error in parsing the argument methods')

    t = toeplitz(x[p-1:-1], np.flip(x[:p]))

    if method in ['classic', 'LS']:
        a = np.linalg.lstsq(-t, x[p:], rcond=None)[0]
    else:
        a = tls(t, -x[p:])

    if sum(np.isnan(a) | np.isinf(a)):
        raise IOError('not solution')

    c = np.hstack((1.0, *a.transpose()))
    r = np.roots(c)[np.newaxis].transpose()

    alpha = np.log(np.abs(r)) / ts
    freq = np.arctan2(np.imag(r), np.real(r)) / (2 * math.pi * ts)

    len_vandermonde = size if method in ['LS', 'TLS'] else p

    z = np.power(
        np.tile(r, len_vandermonde).transpose(), np.array([range(len_vandermonde)]).transpose())

    if method in ['classic', 'LS']:
        h = np.linalg.lstsq(z, x[:len_vandermonde], rcond=None)[0]
    else:
        indeterminate_form = np.sum(np.sum(np.isnan(z) | np.isinf(z)))

        if indeterminate_form:
            raise IOError("not indeterminate form")

        h = tls(z, x[:len_vandermonde])

    amp = np.abs(h)
    theta = np.arctan2(np.imag(h), np.real(h))

    return [amp, alpha, freq, theta]


def matrix_pencil(x, p, ts):

    size = len(x)
    y = hankel(x[:-p], x[-p-1:])

    y1 = y[:, :-1]
    y2 = y[:, 1:]
    l = np.linalg.eig(pinv(y1).dot(y2))[0][np.newaxis].transpose()

    alpha = np.log(np.abs(l)) / ts
    freq = np.arctan2(np.imag(l), np.real(l)) / (2 * np.pi * ts)

    z = np.power(np.tile(l, size).transpose(), np.array([range(size)]).transpose())

    h = np.linalg.lstsq(z, x, rcond=None)[0]

    amp = np.abs(h)
    theta = np.arctan2(np.imag(h), np.real(h))

    return [amp, alpha, freq, theta]
