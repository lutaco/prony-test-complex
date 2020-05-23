import json
import numpy as np
from collections import namedtuple
from itertools import zip_longest
from .clien import client


ALL_TYPE = 'ALL_TYPE'
FIXED_TYPE = 'FIXED_TYPE'

AggData = namedtuple('AggData', ('parameter', 'type', 'data'))


class Analyser(object):

    def __init__(self, solution):
        self.solution = json.loads(solution)
        self.base = client[self.solution['base']]

    def aggregate(self, *params):

        all_params = [x.parameter for x in params if x.type == ALL_TYPE]
        all_params_names = [x.name for x in all_params]

        data = self.base[self.solution['schedule']].find(
            {x.parameter.name: x.data for x in params if x.type == FIXED_TYPE}
        )

        result = np.empty([len(list(x)) for x in all_params], object)
        for row in data:
            result[tuple(map(lambda i: row[i], all_params_names))] = row['result']

        return result.tolist()

    @classmethod
    def recursive_map(cls, action, lst):
        return action(lst) if not isinstance(lst, list) else list(map(
            lambda x: cls.recursive_map(action, x), lst
        ))

    def get_parameters(self, *names):

        if not names:
            names = self.solution['steps_parameters'].keys()

        return [
            Parameter(name, self.base[coll])
            for name, coll in self.solution['steps_parameters'].items()
            if name in names
        ]


class Parameter(object):

    def __init__(self, parameter, collection):
        self.name = parameter
        self.coll = collection

    def __getitem__(self, key):
        return self.coll.find_one({'_id': key})

    def __iter__(self):
        return self.coll.find({})

    def __call__(self, field):
        return self.coll.distinct(field)

    def fixed(self, param_id):
        return AggData(self, FIXED_TYPE, param_id)

    def all(self):
        return AggData(self, ALL_TYPE, None)

    def __str__(self):
        return f"Parameter {self.name}"

    def __repr__(self):
        return f"Parameter {self.name} (collection: {self.coll.full_name})"


def collapse_data(data_lst):
    return np.array(list(zip_longest(*data_lst, fillvalue=None))).transpose()
