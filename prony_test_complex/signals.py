from prony_test_complex.steps import Step
from prony_test_complex.test_signal import sum_signal


class SimpleTestSignal(Step):

    @classmethod
    def step(cls, data):
        return {'start_signal': lambda x: sum_signal(
            [(x, 2.0, omega, 0) for omega in [12.0, 11.5, 8.5]]
        )}


class VerySimpleTestSignal(Step):

    @classmethod
    def step(cls, data):
        return {'start_signal': lambda x: sum_signal(
            [(x, 2.0, omega, 0) for omega in [12.0, 11]]
        )}


class TwoSimpleTestSignal(Step):

    @classmethod
    def step(cls, data):
        return {'start_signal': lambda x: sum_signal(
            [(x, 4.0, 11.0, 0.0), (x, 2.0, 12, 0.0)]
        )}


class TSimpleTestSignal(Step):

    @classmethod
    def step(cls, data):
        return {'start_signal': lambda x: sum_signal(
            [(x, 4.0, 11.0, 0.0), (x, 2.0, 12, 0.0), (x, 1.0, 2.0, 0.0)]
        )}
