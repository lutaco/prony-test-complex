import json
from prony_test_complex.solver import Solver

BASE_NAME = 'db2'
FILE_NAME = f'{BASE_NAME}.json'

with open(FILE_NAME) as f:
    solution = json.load(f)

solver = Solver(json.dumps(solution))
solver.reload()
solver.calculate()
