import matplotlib.pyplot as plt
import numpy as np
from prony_test_complex.test_signal import sum_exp_signal
from prony_test_complex.scortcuts import ls, mpm
import time
from numpy.fft import fft, fftfreq

left = 0.0
right = 0.3
freq = 16000
ll = []
for i in np.linspace(0.1, 1, 50):
    k = 5
    t = np.linspace(left, right, int((right - left) * freq))[::k]

    s = sum_exp_signal([
        (t, 6.4, -6, 800, 0.2),
        (t, 3.4, -5.4, 801, 0.1),
        (t, 3.6, -3.1, 802, 0.5),
        (t, 5.4, -3.2, 802.5, 1.0)
    ])

    fig, (ax1, ax2, ax3) = plt.subplots(3)

    ax1.plot(t, s)

    sp = fft(s)
    freqs = fftfreq(len(t), d=k/freq)
    idx = np.argsort(freqs)
    ps = np.abs(sp)
    ax2.set_xlim(795, 805)
    ax2.stem(freqs[idx], ps[idx], markerfmt=' ', use_line_collection=True)
    print('yay', len(t) * i // 2)

    start_time = time.time()
    params, res = ls(s[np.newaxis].transpose(), int(len(t) * i // 2), k / freq)
    ll.append(time.time() - start_time)
    print(i, " --- %s seconds ---" % (time.time() - start_time))
    amp, alpha, freq_, theta = [x.transpose()[0] for x in params]
    idx = np.argsort(freq_)
    ps = np.abs(amp)

    ax3.set_xlim(795, 805)
    ax3.stem(freq_[idx], ps[idx], markerfmt=' ', use_line_collection=True)
    plt.title(f"{freq // k} / 2 = {freq // k // 2}")
    plt.show()
