import numpy as np
from itertools import starmap
from functools import reduce


def signal(x, amp=1.0, omega=1.0, phi=0):
    return amp * np.sin(x * omega - phi)


def sum_signal(param_set):
    return reduce(lambda a, x: a + x, starmap(signal, param_set))


def exp_signal(x, amp, alpha, freq, theta):
    return amp * np.exp(alpha * x) * np.cos(2 * np.pi * x * freq + theta)


def sum_exp_signal(param_set):
    return reduce(lambda a, x: a + x, starmap(exp_signal, param_set))
