import numpy as np
import importlib
from functools import reduce


def eps(source, res):
    diff = source - res
    return np.sqrt(diff.transpose().dot(diff) / len(diff))


def dynamic_import(abs_module_path, class_name):
    return reduce(lambda a, x: getattr(a, x), class_name.split('.'), importlib.import_module(abs_module_path))
