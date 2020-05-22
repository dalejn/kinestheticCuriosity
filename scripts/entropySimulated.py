from __future__ import division
import numpy as np
from collections import Counter
import math


def entropySimulated(sequence):
    #get frequencies
    tokens_with_count = Counter(sequence)
    counts = np.array(tokens_with_count.values())
    tokens = tokens_with_count.keys()
    ranks = np.arange(1, len(counts) + 1)
    indices = np.argsort(-counts)
    frequencies = np.array(counts[indices])

    total = sum(frequencies)
    ID_entropy = sum([freq / total * math.log(total / freq, 2) for freq in frequencies])

    return ID_entropy