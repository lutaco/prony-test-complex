import numpy as np


def prony_restore_values(amp, alpha, freq, theta, size, ts):

    n = np.tile(range(size), (len(freq), 1))
    k = np.exp(np.tile(alpha, [1, size]) * n * ts)

    y = (np.tile(amp, [1, size]) * k).transpose().dot(np.cos(
        2 * np.pi * ts * np.tile(freq, [1, size]) * n + np.tile(theta, [1, size])
    ))

    return np.diag(y)


def prony_lowpass_filter(amp, alpha, freq, theta, n_comp):

    sort_idx = list(sorted(range(len(freq)), key=lambda i: freq[i]))
    amp, alpha, freq, theta = [
        np.array([x[i] for i in sort_idx]) for x in [amp, alpha, freq, theta]
    ]

    max_comp = len(list(filter(lambda x: x > 0.0, freq)))
    ii = [i for i, x in enumerate(freq) if x < 0.0]
    if not ii:
        ii = [0]

    n_comp = min(max_comp, n_comp)
    fcut = freq[ii.pop() + n_comp]

    ix = [i for i, x in enumerate(freq) if -fcut <= x <= fcut]
    amp_, alpha_, freq_, theta_ = [
        np.array([x[i] for i in ix]) for x in [amp, alpha, freq, theta]
    ]

    return amp_, alpha_, freq_, theta_
