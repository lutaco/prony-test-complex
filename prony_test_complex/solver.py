import json
from importlib import import_module
import time
import pickle
from itertools import count
from collections import deque, defaultdict
from pymongo import MongoClient
from functools import reduce
from numpy import average
from datetime import datetime, timedelta


class StepCache(object):

    def __init__(self, base):
        self.cur_step_key = None
        self.base = base
        self.cache = defaultdict(dict)

    def get(self, step, options):

        name = f"cache_{step['required_parameter']}"
        key = frozenset((x, options[x]) for x in step['cached'])

        if key in self.cache[name]:
            return self.cache[name][key]

        record = self.base[name].find_one({'key': dict(key)})
        if record:
            res = pickle.loads(record['value'])
            self.cache[name][key] = res
            return res

        self.cur_step_key = key, name
        return None

    def commit(self, value):
        if self.cur_step_key:
            key, name = self.cur_step_key
            self.base[name].insert_one({'key': dict(key), 'value': pickle.dumps(value)})
            self.cache[name][key] = value

        self.cur_step_key = None


class Solver(object):

    prognosis_period = 10

    def __init__(self, solution):

        solution = json.loads(solution)
        self.solution = solution

        client = MongoClient()
        self.base = client[solution['base']]

        self.count_documents = self.base[self.solution['schedule']].count_documents({})

        self.parameters = {
            parameter: {x['_id']: x for x in client[solution['base']][collection].find({})}
            for parameter, collection in solution['steps_parameters'].items()
        }
        self.current_iter = count(
            self.base[solution['schedule']].count_documents({'processed': True}))

        self.pipeline = [
            {**action, 'action': self.step_loader(*action['action'])}
            for action in solution['steps']
        ]
        self.times = deque(maxlen=self.prognosis_period)
        self.cache = StepCache(self.base)

    @staticmethod
    def step_loader(m_path, class_name):
        return reduce(lambda a, x: getattr(a, x), class_name.split('.'), import_module(m_path))

    def reload(self):
        self.base[self.solution['schedule']].update_many(
            {'processed': None}, {'$set': {'processed': False}}
        )

    def prognosis(self):
        current_iter = next(self.current_iter)
        d_time = int((self.count_documents - current_iter) * average(self.times))
        t_end = (datetime.now() + timedelta(seconds=d_time)).strftime('%H:%M')
        if current_iter % self.prognosis_period == 0:
            print(f"Решенено {current_iter} / {self.count_documents}\t",
                  f"Примерное время окончания {t_end}\t"
                  f"Среднее время {round(average(self.times), 4)}")

    def step_pipeline(self, options):

        data = {**self.solution['parameters']}
        for step in self.pipeline:

            cached_value = None

            if 'cached' in step:
                cached_value = self.cache.get(step, options)

            if cached_value:
                data.update(cached_value)
                continue

            step_params = {'data': data}
            if 'required_parameter' in step:
                param_name = step['required_parameter']
                step_params['params'] = self.parameters[param_name][options[param_name]]

            res = step['action'].step(**step_params)
            data.update(res)

            if 'cached' in step:
                self.cache.commit(res)

        return {'_id': options['_id']}, {'$set': {'result': data['log'], 'processed': True}}

    def calculate(self):
        options = None
        print('start solution')
        try:
            for options in self.base[self.solution['schedule']].find({'processed': False}):

                start_time = time.time()
                self.base[self.solution['schedule']].update(*self.step_pipeline(options))
                self.times.append(time.time() - start_time)
                self.prognosis()

        except KeyboardInterrupt:
            if options:
                self.base[self.solution['schedule']].update(
                    {'_id': options['_id']}, {'$set': {'processed': False}})
            print('stop')
        else:
            print('End Solution')
