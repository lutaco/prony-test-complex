import json
import numpy as np
from prony_test_complex import builder, steps, signals, scortcuts

BASE_NAME = 'db1s'
FILE_NAME = f'../solutions/{BASE_NAME}.json'


if input('Начать новый расчет? [Y/n]: ').lower() == 'y':

    test_builder = builder.Builder(
        BASE_NAME, {'range': [0.0, 0.3], 'fs': 40000, 'ex_fs': 10000, 'relative': True}
    )

    test_builder.add_steps([
        signals.SOneSimpleTestSignal(),
        steps.CreateSignal(),
        steps.SNoise(np.linspace(0.0, 0.15, 31)),
        steps.Filters([
            ('empty', scortcuts.empty_filter),
            ('wiener', scortcuts.win_filter),
            ('batter', scortcuts.x_but_filter),
        ]),
        steps.SDecimation((2, 3, 5, 7)),
        steps.ComponentsCount(np.linspace(1, 90, 49)),
        steps.SComputing([
            ('ls', scortcuts.s_ls),
            ('mpm', scortcuts.s_mpm)
        ]),
        steps.Epsilon(),
        steps.Save()
    ])

    solution = test_builder.get_solution()

    with open(FILE_NAME, 'w') as f:
        json.dump(solution, f, indent=4)
