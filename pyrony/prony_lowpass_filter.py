import numpy as np
from pyrony import settings


def prony_restore_values(Amp, alfa, freq, theta, N, Ts):

    n = np.tile(range(N), (len(freq), 1))
    k = np.exp(np.tile(alfa, [1, N]) * n * Ts)

    Y = (np.tile(Amp, [1, N]) * k).transpose().dot(np.cos(
        2 * np.pi * Ts * np.tile(freq, [1, N]) * n + np.tile(theta, [1, N])
    ))

    return np.diag(Y)


def prony_lowpass_filter(Amp, alpha, freq, theta, N, Ts, Ncomp):

    sort_idx = list(sorted(range(len(freq)), key=lambda i: freq[i]))
    Amp, alpha, freq, theta = [
        np.array([x[i] for i in sort_idx]) for x in [Amp, alpha, freq, theta]
    ]

    max_comp = len(list(filter(lambda x: x > 0.0, freq)))
    ii = [i for i, x in enumerate(freq) if x < 0.0]
    if not ii:
        ii = [0]
    Ncomp = min(max_comp, Ncomp)
    fcut = freq[ii.pop() + Ncomp]

    ix = [i for i, x in enumerate(freq) if -fcut <= x <= fcut]
    Amp_, alpha_, freq_, theta_ = [
        np.array([x[i] for i in ix]) for x in [Amp, alpha, freq, theta]
    ]

    return Amp_, alpha_, freq_, theta_
