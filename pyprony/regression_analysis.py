import numpy as np
from pyprony import settings


def tls(a, b):

    m, n = a.shape
    z = np.hstack((a, b))

    u, s, vt = np.linalg.svd(z)
    v = vt.transpose()
    vxy = v[:n, n:]
    vyy = v[n:, n:]

    if np.isclose(vyy, settings.PRECISION):
        raise IOError('not TLS solution')

    return - vxy / vyy
