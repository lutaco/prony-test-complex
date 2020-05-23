import numpy as np
from pyrony import settings


def tls(A, b):

    m, n = A.shape
    Z = np.hstack((A, b))

    U, S, Vt = np.linalg.svd(Z)
    V = Vt.transpose()
    Vxy = V[:n, n:]
    Vyy = V[n:, n:]

    if np.isclose(Vyy, settings.PRECISION):
        raise IOError('not TLS solution')

    return - Vxy / Vyy
