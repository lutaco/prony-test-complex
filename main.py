import json
import numpy as np
from prony_test_complex import builder, steps, signals, scortcuts

from prony_test_complex.solver import Solver


BUILD = True

BASE_NAME = 'db1'
FILE_NAME = f'{BASE_NAME}.json'


def eps_filter(x):
    eps = float('inf') if x is None else x['eps']
    return eps if eps < 1.0 else None


if BUILD and input('Начать новый расчет? [Y/n]: ').lower() == 'y':

    test_builder = builder.Builder(
        BASE_NAME, {'range': [0.2, 0.5], 'fs': 18000, 'ex_fs': 1500}
    )

    test_builder.add_steps([
        signals.OneSimpleTestSignal(),
        steps.CreateSignal(),
        steps.Noise(np.linspace(0.0, 0.3, 10), cached=[steps.Noise]),
        steps.Decimation((6, 7, 8)),
        steps.Filters([
            ('empty', scortcuts.empty_filter),
            ('wiener', scortcuts.win_filter),
            ('butter', scortcuts.but_filter),
        ], cached=[steps.Noise, steps.Decimation]),
        steps.ComponentsCount(np.linspace(1, 100, 20)),
        steps.Computing([
            ('ls', scortcuts.ls),
            ('mpm', scortcuts.mpm)
        ]),
        steps.Epsilon(),
        steps.Save()
    ])

    solution = test_builder.get_solution()

    with open(FILE_NAME, 'w') as f:
        json.dump(solution, f, indent=4)

with open(FILE_NAME) as f:
    solution = json.load(f)

solver = Solver(json.dumps(solution))
solver.reload()
solver.calculate()
