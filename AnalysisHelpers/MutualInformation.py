from itertools import compress
from math import log, sqrt

import scipy

log2 = lambda x: log(x, 2)
from scipy import histogram, digitize, stats
from collections import defaultdict
import numpy as np


def mutual_information(x, y):
    enty, normenty = entropy(y)
    entx, normentx = entropy(x)
    mi = enty - conditional_entropy(x, y)
    # normmi : the results between 0 (no mutual information) and 1 (perfect correlation)
    normmi = mi / sqrt(entx * enty)
    return mi, normmi


# H(Y|X)
def conditional_entropy(x, y):
    hx, bx = histogram(x, bins=int(len(x) / 10), density=True)

    Py = compute_distribution(y)
    # Px = compute_distribution(digitize(x, bx))
    Px = compute_distribution(x)

    res = 0
    for ey in set(y):
        # P(X | Y)
        # x1 = x[y == ey]
        try:
            x1 = list(compress(x, y == ey))
        except TypeError:
            x1 = list(compress(x, np.asarray([y == ey])))
        # condPxy = compute_distribution(digitize(x1, bx))
        condPxy = compute_distribution(x1)

        for k in condPxy:
            v = condPxy[k]
            res += (v * Py[ey] * (log2(Px[k]) - log2(v * Py[ey])))
    return res


def entropy(y):
    Py = compute_distribution(y)

    # res = 0.0
    # for k in Py:
    #     v = Py[k]
    #     res += v * log2(v)
    #
    # ent = -res
    ent = scipy.stats.entropy([Py[p] for p in Py], base=2)
    norment = ent / log2(len(Py))
    return ent, norment


def compute_distribution(v):
    d = defaultdict(int)
    for e in v: d[e] += 1
    s = float(sum(d.values()))
    return dict((k, v / s) for k, v in d.items())
