import pymongo

from itertools import product, count
from .settings import client


class Builder(object):

    def __init__(self, base, settings=None):
        self.db = client[base]
        self.base = base
        self.steps = []
        self.steps_parameters = {}
        self.settings = settings or {}

    def add_step(self, step):
        self.steps.append(step)

    def build_step(self, step):

        step_settings = {'action': (step.__class__.__module__, step.__class__.__name__)}
        if hasattr(step, 'representative'):
            collection_name = f"collection_{step.representative}"
            self.db[collection_name].insert_many(
                {'_id': i, **value} for i, value in enumerate(step.get_parameters())
            )
            step_settings.update({'required_parameter': step.representative})
            if hasattr(step, 'cached'):
                step_settings.update({'cached': tuple(x.representative for x in step.cached)})

            self.steps_parameters[step.representative] = collection_name

            cache_name = f"cache_{step.representative}"
            self.db[cache_name].create_index([('set_key', pymongo.ASCENDING)], unique=True)

        return step_settings

    def add_steps(self, steps):
        for step in steps:
            self.add_step(step)

    def get_solution(self):
        assembled_steps = [self.build_step(step) for step in self.steps]
        steps = [x['required_parameter'] for x in assembled_steps if 'required_parameter' in x]
        values_steps = map(lambda x: self.db[self.steps_parameters[x]].distinct('_id'), steps)
        id_counter = count(0)
        self.db.collection_schedule.insert_many(
            {'_id': next(id_counter), 'processed': False, **dict(zip(steps, x))}
            for x in product(*values_steps)
        )
        return {
            'base': self.base,
            'schedule': 'collection_schedule',
            'steps': assembled_steps,
            'parameters': self.settings,
            'steps_parameters': self.steps_parameters
        }
