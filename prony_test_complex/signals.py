from prony_test_complex.steps import Step
from prony_test_complex.test_signal import sum_exp_signal


class OneSimpleTestSignal(Step):

    @classmethod
    def step(cls, data):
        return {'start_signal': lambda t: sum_exp_signal(
            [(t, 2, 0, 1000, 1.4), (t, 1, 0, 1001, 1.3), (t, 3, 0, 1002, 0.2)]
        )}


class TwoSimpleTestSignal(Step):

    @classmethod
    def step(cls, data):
        return {'start_signal': lambda t: sum_exp_signal([
            (t, 3.5, 0, 1000, 0.4),
            (t, 5, 0, 1001, 1.1),
            (t, 3.4, 0, 1002, 0.5),
            (t, 5.2, 0, 1002.5, 1.0)
        ])}


class OneExpTestSignal(Step):

    @classmethod
    def step(cls, data):
        return {'start_signal': lambda t: sum_exp_signal([
            (t, 3.5, -4.4, 1000, 0.4), (t, 1, 0.1, 1001, 1.1), (t, 2.5, -4.2, 1002, 0.8)
        ])}


class TwoExpTestSignal(Step):

    @classmethod
    def step(cls, data):
        return {'start_signal': lambda t: sum_exp_signal([
            (t, 6.4, -6, 800, 0.2),
            (t, 3.4, -5.4, 801, 0.1),
            (t, 3.6, -3.1, 802, 0.5),
            (t, 5.4, -3.2, 802.5, 1.0)
        ])}
