import numpy as np
from scipy.optimize import curve_fit
# import matplotlib.pyplot as plt


def heapsSimulated(sequence):
    # Define the model for an exponential distribution
    def myExpFunc(x, a, b):
        return a * np.power(x, b)

    allNodes = []
    totalLength = []
    uniqueLength = []

    for node in sequence:  # for each word in the whole corpus
        allNodes.append(node)  # add the word to a cummulative list
        totalLength.append(len(allNodes))  # save the length of the cumulative list so far
        uniqueLength.append(len(set(allNodes)))  # save the number of unique words in the cumulative list so far

    #fig = plt.loglog(totalLength, uniqueLength)

    x = np.array(totalLength)
    y = np.array(uniqueLength)

    # Do the fitting with least-squares

    try:
        popt, pcov = curve_fit(myExpFunc, x, y)
        return popt[1]
    except RuntimeError:  # if can't fit with exponential distribution, assume 0 (horizontal)
        return 0
