import collections
from itertools import compress
from math import log, sqrt
import numpy as np
import scipy
from scipy import stats


# link to formulas : http://www.scholarpedia.org/article/Mutual_information#Interpretation
# and : https://en.wikipedia.org/wiki/Mutual_information#Relation_to_other_quantities


def mylog(x):
    return log(x, 2)  # (base 2)
    # return log(x)  # the natural logarithm (base e). Be careful some part of the code may be corrupted !


def computMutualInformation4Continuous(fx, fy, per=2):
    x = [round(p, per) for p in fx]
    y = [round(p, per) for p in fy]

    entx, normentx = computeEntropy4Discrete(x)
    enty, normenty = computeEntropy4Discrete(y)
    mi = enty - computConditionalEntropy4Discrete(x, y)
    # normmi : the results between 0 (no mutual information) and 1 (perfect correlation)
    normmi = mi / sqrt(entx * enty)
    return mi, normmi


def computeEntropy4Continuous(fy, per=2):
    return computeEntropy4Discrete([round(p, per) for p in fy])


def computeEntropy4Continuous2(fv, per=2):
    return computeEntropy4Discrete2([round(p, per) for p in fv])


def computMutualInformation4Discrete(x, y):
    enty, normenty = computeEntropy4Discrete(y)
    entx, normentx = computeEntropy4Discrete(x)
    mi = enty - computConditionalEntropy4Discrete(x, y)
    # normmi : the results between 0 (no mutual information) and 1 (perfect correlation)
    normmi = mi / sqrt(entx * enty)
    return mi, normmi


# H(Y|X)
def computConditionalEntropy4Discrete(x, y):
    Py = computeDistribution4Discrete(y)
    Px = computeDistribution4Discrete(x)

    res = 0
    for ey in set(y):
        # P(X | Y)
        # x1 = x[y == ey]
        try:
            x1 = list(compress(x, np.asarray(y == ey)))
        except TypeError:
            x1 = list(compress(x, np.asarray([y == ey])))
        # condPxy = compute_distribution(digitize(x1, bx))
        condPxy = computeDistribution4Discrete(x1)

        for k in condPxy:
            v = condPxy[k]
            res += (v * Py[ey] * (mylog(Px[k]) - mylog(v * Py[ey])))
    return res


def computeEntropy4Discrete(y):
    Py = computeDistribution4Discrete(y)

    # plt.hist([Py[p] for p in Py], bins=[p for p in Py])
    # plt.bar(np.arange(0, len(Py)), [Py[p] for p in Py])
    # plt.xticks(np.arange(0, len(Py)), [p for p in Py])
    # plt.show()

    # res = 0.0
    # for k in Py:
    #     v = Py[k]
    #     res += v * log2(v)
    #
    # ent = -res
    ent = scipy.stats.entropy([Py[p] for p in Py], base=2)
    norment = ent / mylog(len(Py))
    return ent, norment


# this function copied from sklearn.metrics package
def computeEntropy4Discrete2(v):
    """Calculates the entropy for a labeling."""
    if len(v) == 0:
        return 1.0
    label_idx = np.unique(v, return_inverse=True)[1]
    pi = np.bincount(label_idx).astype(np.float64)
    pi = pi[pi > 0]
    pi_sum = np.sum(pi)
    # log(a / b) should be calculated as log(a) - log(b) for possible loss of precision
    ent = -np.sum((pi / pi_sum) * (np.log2(pi) - mylog(pi_sum)))
    norment = ent / mylog(len(pi))
    return ent, norment


def computeDistribution4Discrete(v):
    d = {}
    for e in v:
        if e not in d:
            d[e] = 0
        d[e] += 1
    s = float(sum(d.values()))
    for t in d:
        d[t] /= s
    od = collections.OrderedDict(sorted(d.items()))
    return od
