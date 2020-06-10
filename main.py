import json
from prony_test_complex.solver import Solver

BASE_NAME = 'db3s'
FILE_NAME = f'solutions/{BASE_NAME}.json'

with open(FILE_NAME) as f:
    solution = json.load(f)

solver = Solver(json.dumps(solution))
solver.reload()
solver.calculate()
