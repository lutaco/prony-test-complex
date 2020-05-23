import numpy as np
from itertools import starmap
from functools import reduce


def exp_signal(x, amp, alpha, freq, theta):
    return amp * np.exp(alpha * x) * np.cos(2 * np.pi * x * freq + theta)


def sum_exp_signal(param_set):
    return reduce(lambda a, x: a + x, starmap(exp_signal, param_set))
