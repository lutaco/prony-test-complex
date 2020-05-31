import warnings
import pickle
import numpy as np
from abc import abstractmethod, ABC


class Step(ABC):

    def __init__(self, cached=False):
        if cached:
            self.cached = cached

    @abstractmethod
    def step(self, data):
        pass


class RangeStep(ABC):

    def __init__(self, cached=False):
        if cached:
            self.cached = cached

    @abstractmethod
    def representative(self):
        pass

    @abstractmethod
    def step(self, data, params):
        pass

    @abstractmethod
    def get_parameters(self):
        pass


class EasyParametersMixin(ABC):

    @abstractmethod
    def representative(self):
        pass

    def __init__(self, parameters, **options):
        super().__init__(**options)
        self.parameters = parameters

    def get_parameters(self):
        return ({self.representative: x} for x in self.parameters)


class CreateSignal(Step):

    @classmethod
    def step(cls, data):
        left, right = data['range']
        t = np.linspace(left, right, int((right - left) * data['fs']))
        source = data['start_signal'](t)
        return {'source': source}


class Noise(EasyParametersMixin, RangeStep):

    representative = 'snr'

    @classmethod
    def step(cls, data, params):
        signal = data['source']
        noise_m = params['snr'] * np.sqrt(signal.dot(signal) / len(signal))
        noise = np.random.normal(0, noise_m, len(signal))
        res = signal + noise
        return {'signal': res}


class Filters(EasyParametersMixin, RangeStep):

    representative = 'filter'

    @classmethod
    def step(cls, data, params):
        result = pickle.loads(params['shortcut'])(data)
        return {'signal': result}

    def get_parameters(self):
        return ({'filter': name, 'shortcut': pickle.dumps(flt)} for name, flt in self.parameters)


class Decimation(EasyParametersMixin, RangeStep):

    representative = 'step'

    @classmethod
    def step(cls, data, params):
        new_fs = data['fs'] / params['step']
        return {
            'signal': data['signal'][::params['step']],
            'fs': new_fs, 'source': data['source'][::params['step']]
        }


class SDecimation(EasyParametersMixin, RangeStep):

    representative = 'step'

    @classmethod
    def step(cls, data, params):
        new_fs = data['fs'] / params['step']
        return {
            'signal': data['signal'][::params['step']],
            'new_fs': new_fs
        }


class ComponentsCount(EasyParametersMixin, RangeStep):

    representative = 'p'

    @classmethod
    def step(cls, data, params):
        return {'p': params['p']}


class SComputing(EasyParametersMixin, RangeStep):
    representative = 's_method'

    @classmethod
    def step(cls, data, params):
        try:
            signal = data['signal']

            p = data['p']
            if data.get('relative', False):
                p = int(data['p'] * len(signal) // 200)

            params, restore_method = pickle.loads(
                params['approximate'])(signal[np.newaxis].transpose(), p, 1 / data['new_fs'])

            restore = restore_method(*params, len(data['source']), 1 / data['fs'])
            success = True

        except (np.linalg.LinAlgError, IOError, ValueError, RuntimeWarning):
            success, restore = None, None

        return {'success': bool(success), 'result': None if not success else {
            'params': params, 'restore': restore
        }}

    def get_parameters(self):
        return (
            {'method': name, 'approximate': pickle.dumps(method)}
            for name, method in self.parameters
        )


class Computing(EasyParametersMixin, RangeStep):

    representative = 'method'

    @classmethod
    def step(cls, data, params):
        try:
            signal = data['signal']

            p = data['p']
            if data.get('relative', False):
                p = data['p'] * len(signal) // 200

            result = pickle.loads(
                params['approximate'])(signal[np.newaxis].transpose(), int(p), 1 / data['fs'])
        except (np.linalg.LinAlgError, IOError, ValueError, RuntimeWarning):
            result = None

        return {'success': bool(result), 'result': None if not result else {
            'params': result[0], 'restore': result[1]
        }}

    def get_parameters(self):
        return (
            {'method': name, 'approximate': pickle.dumps(method)}
            for name, method in self.parameters
        )


class Epsilon(Step):

    @classmethod
    def step(cls, data):

        if not data['success']:
            return data

        signal = data['result']['restore']
        diff = signal - data['source']
        return {'eps': np.sqrt(diff[np.newaxis].dot(diff)[0]) / len(diff)}


class Save(Step):

    @classmethod
    def step(cls, data):
        return {'log': None if not data['success'] else {
            'eps': data['eps'],
            'signal': data['signal'].dumps(),
            'params': list(map(lambda x: x.dumps(), data['result']['params'])),
        }}
