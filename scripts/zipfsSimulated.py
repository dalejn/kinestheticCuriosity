import numpy as np
import powerlaw
from collections import Counter


def zipfsSimulated(sequence):
    tokens_with_count = Counter(sequence)
    counts = np.array(tokens_with_count.values())
    indices = np.argsort(-counts)
    frequencies = counts[indices]
    fit = powerlaw.Fit(frequencies, discrete=True, verbose=False)

    try:
        return fit.power_law.alpha
    except RuntimeError:  # if can't fit with exponential distribution, assume 0 (horizontal)
        return 0
