import json
import pickle
import numpy as np
import matplotlib.pyplot as plt

from prony_test_complex import builder, steps, signals, scortcuts
from math import pi
from prony_test_complex.signals import TwoSimpleTestSignal
from pymongo import MongoClient
# from .pyrony import prony_lowpass_filter, approximation

from prony_test_complex.solver import Solver
from prony_test_complex.analyser import Analyser, collapse_data
from prony_test_complex.scortcuts import ls, mpm
from prony_test_complex.test_signal import sum_signal
from itertools import count, product


BUILD = True

BASE_NAME = 'kuasdfasdfrs_test'
FILE_NAME = f'{BASE_NAME}.json'


def eps_filter(x):
    eps = float('inf') if x is None else x['eps']
    return eps if eps < 1.0 else None


if BUILD and input('Начать новый расчет? Данные предыдущего будут удалены [Y/n]: ').lower() == 'y':

    test_builder = builder.Builder(
        BASE_NAME, {'range': [-5 * pi, 5 * pi], 'size': 400})

    test_builder.add_steps([
        signals.TwoSimpleTestSignal(),
        steps.Offset(np.linspace(0.0, 1., 20)),
        steps.Noise(np.linspace(0.0, 0.3, 60), cached=[steps.Noise]),
        steps.ComponentsCount(list(range(10, 200, 5))),
        steps.Computing([
            ('ls', scortcuts.ls),
        ]),
        steps.Epsilon(),
        steps.Save()
    ])

    solution = test_builder.get_solution()

    with open(FILE_NAME, 'w') as f:
        json.dump(solution, f, indent=4)

with open(FILE_NAME) as f:
    solution = json.load(f)

client = MongoClient()
db = client[solution['base']]

solver = Solver(json.dumps(solution))
solver.reload()
solver.calculate()

anal = Analyser(json.dumps(solution))

offset, sigma, p, method = anal.get_parameters()
# res = anal.aggregate(sigma.all(), p.all(), method.fixed(0))
# filtered_res = anal.recursive_map(eps_filter, res)
#
# fig, axes = plt.subplots(figsize=(8, 6))
# csn = axes.contourf(p('p'), sigma('sigma_k'), filtered_res, levels=12)
# axes.set_xlabel('p')
# axes.set_ylabel('sigma scale')
# fig.colorbar(csn)
# plt.show()
#
# plot_data = anal.aggregate(sigma.fixed(19), p.all(), method.fixed(0))[3:]
# plot_data = list(map(eps_filter, plot_data))
# fig, axes = plt.subplots(figsize=(8, 6))
# axes.plot(list(p('p'))[3:], plot_data, 'bo', markersize=3)
# axes.set_xlabel(r'$p$')
# axes.set_ylabel(r'$\epsilon$')
# plt.show()


# plt.title(f'Завимиость погрешности от p ({m_i["method"]}) filter {f_i["filter"]}')

# for m_i, f_i in product(list(method), list(filt)):
#     res = anal.aggregate(sigma.fixed(sgm), p.all(), filt.fixed(f_i['_id']), method.fixed(m_i['_id']))
#     plot_data = [x['eps'] if x is not None else None for x in res]
#     _, axes = plt.subplots(figsize=(12, 8))
#     axes.set_xlabel('p')
#     axes.set_ylabel('eps')
#     plt.ylim(0, 0.025)
#     plt.plot(list(p('p')), plot_data, 'bo')
#     plt.title(f'Завимиость погрешности от p ({m_i["method"]}) filter {f_i["filter"]}')
#     plt.show()

# m_i = 0
# f_i = 0
# res = anal.aggregate(sigma.fixed(19), p.all(), method.fixed(0))
# for name, idx in [('Amp', 0), ('Freq', 2)]:
#
#     data = [
#         pickle.loads(x['params'][idx]) if x is not None else np.array([[None]]) for x in res]
#
#     f_data = [
#         pickle.loads(x['params'][2]) if x is not None else np.array([[None]]) for x in res]
#
#     data_list = [data_item.reshape(len(data_item)).tolist() for data_item in data]
#
#     fig, axes = plt.subplots(figsize=(7, 6))
#     axes.set_xlabel("$p$")
#     axes.set_ylabel(f"${name}$")
#     plt.plot(list(p('p')), collapse_data(data_list), 'bo', markersize=2.0)
#
#     if idx == 0:
#         plt.ylim(-0.05, 3)
#         plt.plot(list(p('p')), [1] * len(list(p)), 'r', linewidth=1.0)
#         plt.plot(list(p('p')), [2] * len(list(p)), 'r', linewidth=1.0)
#
#     # if idx == 1:
#     #     plt.ylim(-20, 10)
#
#     if idx == 2:
#         plt.ylim(-0.1, 15)
#         plt.plot(list(p('p')), [11] * len(list(p)), 'r', linewidth=1.0)
#         plt.plot(list(p('p')), [12] * len(list(p)), 'r', linewidth=1.0)
#
#     # if idx == 3:
#     #     plt.ylim(0.5, 2)
#
#     plt.show()
#
# # # #     #
#     plot_data = [x['eps'] if x is not None else None for x in res]
#     _, axes = plt.subplots(figsize=(12, 8))
#     axes.set_xlabel('p')
#     axes.set_ylabel('eps')
#     plt.plot(list(p('p')), plot_data, 'bo')
#     plt.title(f'Завимиость погрешности от p ({method[m_i]["method"]}) filter {filt[f_i]["filter"]}')
#     plt.show()
#     res = anal.aggregate(sigma.fixed(2), p.fixed(p_i), filt.fixed(f_i), method.fixed(m_i))
#     a = res['params'][0]
#     f = res['params'][2]
#     a = pickle.loads(a)
#     f = pickle.loads(f)
#     a = a.transpose().tolist()[0]
#     f = f.transpose().tolist()[0]
#     plt.stem(f, a, markerfmt=' ')
#     plt.xlim(0, 30)
#     plt.ylim(0, 6)
#     plt.show()
#
# x = np.linspace(-5 * np.pi, 5 * np.pi, 1000)
#
# source = TwoSimpleTestSignal.step({})['start_signal'](x)
#
# res = anal.aggregate(sigma.fixed(sgm), p.fixed(32), filt.fixed(1), method.fixed(1))
#
# rr = pickle.loads(res['restore'])
# ss = pickle.loads(res['signal'])
#
# plt.plot(source, label='source')
# plt.plot(rr, label='resote')
# plt.legend()
# plt.show()
#
# plt.plot(source, label='source')
# plt.plot(ss, label='noise')
# plt.legend()
# plt.show()


# t = ss
# sp = np.fft.fft(t)
# freq = np.fft.fftfreq(len(x)) / (10 * np.pi / len(x) / (2 * np.pi))
# plt.stem(freq, sp.real, markerfmt=' ')
# plt.xlim(0, 15)
# plt.ylim(-200, 200)
# plt.show()
# #
# # for m_i, f_i in product(list(method), list(filt)):
# res = anal.aggregate(sigma.fixed(19), p.all(), method.fixed(0))[26:]
# # a, t, f, ph = [pickle.loads(x).transpose().tolist()[0] for x in res['params']]
# # fi = sorted(list(range(len(f))), key=lambda i: f[i])
# #
# f = [
#     pickle.loads(x['params'][2]) if x is not None else np.array([[None]]) for x in res][20:]
#
# a = [
#         pickle.loads(x['params'][0]) if x is not None else np.array([[None]]) for x in res][20:]
#
# from collections import defaultdict
# yres = defaultdict(float)
#
# for aai, ffi in zip(a, f):
#     for ai, fi in zip(aai, ffi):
#         yres[int(fi * 100)] += ai[0]
#
# xres, yres = list(zip(*sorted(yres.items())))
# #
# # # print
# # fx = anal.recursive_map(lambda x: int(x * 100), sum(f, []))
# # ax = anal.recursive_map(lambda x: int(x * 100), sum(a, []))
# plt.stem([x / 100 for x in xres], yres, markerfmt=' ', use_line_collection=True)
# # plt.xlim(0.1, 70)
# # plt.ylim(0, 100)
# plt.legend()
# plt.show()
#
# res = anal.aggregate(sigma.fixed(49), p.all(), method.fixed(0))
# from collections import Counter
# for name, idx in [('Amp', 0), ('Freq', 2)]:
#
#     data = [
#         pickle.loads(x['params'][idx]) if x is not None else np.array([[None]]) for x in res][20:60]
#
#     f_data = [
#         pickle.loads(x['params'][2]) if x is not None else np.array([[None]]) for x in res]
#
#     _, axes = plt.subplots(figsize=(7, 6))
#     if idx == 0:
#         data_list = [data_item.reshape(len(data_item)).tolist() for data_item in data]
#         xx = anal.recursive_map(lambda x: int(x * 50), sum(data_list, []))
#         plt.ylim(0, 800)
#         plt.xlim(0.1, 3)
#         plt.plot()
#         x = set(xx)
#         xxx = Counter(xx)
#
#         axes.stem([x / 50 for x in sorted(list(x))], [xxx[i] for i in sorted(list(x))], markerfmt=' ', use_line_collection=True)
#         plt.show()
#
#     if idx == 2:
#         data_list = [data_item.reshape(len(data_item)).tolist() for data_item in data]
#         xx = anal.recursive_map(lambda x: int(x * 100), sum(data_list, []))
#         plt.xlim(0, 20)
#         plt.plot()
#         x = set(xx)
#         xxx = Counter(xx)
#
#         axes.stem([x / 100 for x in sorted(list(x))], [xxx[i] for i in sorted(list(x))], markerfmt=' ', use_line_collection=True)
#         plt.show()
#
