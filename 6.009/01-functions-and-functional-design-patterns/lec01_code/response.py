import math
import matplotlib.pyplot as plt

def sine_response(lo, hi, step):
    xs = []
    ys = []
    cur = lo
    while cur <= hi:
        xs.append(cur)
        ys.append(math.sin(cur))
        cur += step
    plt.plot(xs, ys)
