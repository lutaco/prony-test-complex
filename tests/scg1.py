import json
import numpy as np
from prony_test_complex import builder, steps, signals, scortcuts

BASE_NAME = 'db1scg'
FILE_NAME = f'../solutions/{BASE_NAME}.json'


if input('Начать новый расчет? [Y/n]: ').lower() == 'y':

    test_builder = builder.Builder(
        BASE_NAME,  {'relative': True, 'file_name': 'scg_part1.tsv'}
    )

    test_builder.add_steps([
        signals.LoadRealSignal(),
        steps.Filters([
            ('empty', scortcuts.empty_filter),
            ('wiener', scortcuts.win_filter),
        ]),
        steps.ComponentsCount(np.linspace(1, 99, 49)),
        steps.RComputing([
            ('ls', scortcuts.s_ls),
            ('mpm', scortcuts.s_mpm)
        ]),
        steps.RSave()
    ])

    solution = test_builder.get_solution()

    with open(FILE_NAME, 'w') as f:
        json.dump(solution, f, indent=4)
