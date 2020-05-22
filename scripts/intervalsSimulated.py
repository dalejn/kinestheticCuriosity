import numpy as np
import powerlaw
from collections import Counter
from functools import partial


def list_duplicates_of(seq, item):
    start_at = -1
    locs = []
    while True:
        try:
            loc = seq.index(item, start_at+1)
        except ValueError:
            break
        else:
            locs.append(loc)
            start_at = loc
    return locs


def intervalsSimulated(sequence):
    # Find duplicates in the list of words
    dups_in_source = partial(list_duplicates_of, sequence)
    doc_intervals = []

    for node in sequence:

        # Get index of duplicates
        indices = dups_in_source(node) # find index of duplicates of a particular node vlaue

        # Calculate the difference between each successive pair of indices
        calc_intervals = [j - i for i, j in zip(indices[:-1], indices[1:])]
        # if there's only 1 occurrence, returns empty

        # Save intervals as nested list
        doc_intervals.append(calc_intervals)

    # Flatten nested list to get distribution of intervals
    doc_intervals = [item for sublist in doc_intervals for item in sublist]

    # Count each token and calculate frequencies
    tokens_with_count = Counter(doc_intervals)
    counts = np.array(tokens_with_count.values())  # count the number of times each interval value occurs
    indices = np.argsort(-counts)  # get the indices that sorts the counts in descending order
    frequencies = counts[indices]  # get frequencies in descending order
    fit = powerlaw.Fit(frequencies, discrete=True, verbose=False)

    try:
        return fit.power_law.alpha
    except RuntimeError:  # if can't fit with exponential distribution, assume 0 (horizontal)
        return 0
