from __future__ import division
from heapsSimulated import heapsSimulated
from entropySimulated import entropySimulated
from zipfsSimulated import zipfsSimulated
from intervalsSimulated import intervalsSimulated
from errwLevyFunction import generateLevy
import numpy as np
from scipy import stats
from datetime import datetime
import random
import deap.benchmarks
from deap import base
from deap import creator
from deap import tools
from deap import algorithms
from scoop import futures
import pickle
import copy
import glob
import networkx as nx

subjectNumber = 0
path = "/data/"
foldList = []
subjectList = []
for (foldFile,subjectFile) in zip(sorted(glob.glob(path+"kFolds/*Train.txt")), sorted(glob.glob(path+"underlyingNetworks/*.txt")*3)):
    foldList.append(foldFile)
    subjectList.append(subjectFile)
                                                                                 
filePath = foldList[subjectNumber]
underlyingPath = subjectList[subjectNumber]
empiricalSequence = np.loadtxt(filePath).tolist()
empiricalSequenceLength = len(empiricalSequence)
heaps = heapsSimulated(empiricalSequence)
entropy = entropySimulated(empiricalSequence)
zipfs = zipfsSimulated(empiricalSequence)
intervals = intervalsSimulated(empiricalSequence)
individualsToTest = np.loadtxt(path+'individualsForTesting.txt')
individualsToTest = np.repeat(individualsToTest,repeats=3,axis=0)

G = nx.from_numpy_matrix(np.genfromtxt(underlyingPath))  # load squareform connectivity matrix as numpy matrix
if not nx.is_connected(G):
    largestConnectedComponent = max(nx.connected_components(G), key=len)
    G = G.subgraph(largestConnectedComponent)
diam = nx.diameter(nx.minimum_spanning_tree(G))
    
###############################
# Define evaluation functions #
###############################


def f1(sequences):  # objective function, computing KS statistic between simulated and empirical CDFs
    print datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " computing Heaps cost"
    heapsSim = heapsSimulated(sequences)  # compute heaps for each simulated draft
    return (heapsSim-heaps)**2


def f2(sequences):  # objective function, computing KS statistic between simulated and empirical CDFs
    print datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " computing entropy cost"
    entropySim = entropySimulated(sequences)  # compute entropy for each simulated draft
    return (entropySim-entropy)**2


def f3(sequences):  # objective function, computing KS statistic between simulated and empirical CDFs
    print datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " computing Zipfs cost"
    zipfsSim = zipfsSimulated(sequences)  # compute zipfs for each simulated draft
    return (zipfsSim-zipfs)**2


def f4(sequences):  # objective function, computing KS statistic between simulated and empirical CDFs
    print datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " computing interevent time cost"
    intervalsSim = intervalsSimulated(sequences)  # compute intervals for each simulated draft
    return (intervalsSim-intervals)**2

def evaluate(Individual):  # evaluating each individual, returning performance by objective functions
    print datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " generating individuals"
    reinforcementParam, levyParam = Individual[0], Individual[1]  # define parameters to optimize
    sequences = generateLevy(empiricalSequenceLength, reinforcementParam, levyParam, G, diam)
    return f1(sequences), f2(sequences), f3(sequences), f4(sequences)  # compute cost functions

####################
# General settings #
####################

IND_SIZE = 2  # number of parameters per individual
LOWER = [0, 1]  # set lower bounds for reinforcement and levy, respectively
UPPER = [100, 3]  # set upper bounds for reinforcement and levy, respectively
POP_SIZE = 50  # number of individuals per population
OFFSPRING_SIZE = 50  # number of individuals for next generation
NGEN = 100  # number of generations
MU = OFFSPRING_SIZE  # number of individuals to select for next generation
LAMBDA = OFFSPRING_SIZE  # number of children to produce at each generation
CXPB = 0.8  # the probability that an offspring is produced by crossover
MUTPB = 0.2  # the probability that an offspring is produced by mutation
ETA = 10  # crowding degree of the crossover (high value produces children resembling parents
# acts as denominator of mutation amount and crossover probability)
SELECTOR = "NSGA2"  # https://github.com/DEAP/deap/blob/master/deap/tools/emo.py


def uniform(lower_list, upper_list, dimensions):  # draw parameter uniform distribution space (params have equal prob)
    """Fill array """

    if hasattr(lower_list, '__iter__'):
        return [random.uniform(lower, upper) for lower, upper in
                zip(lower_list, upper_list)]
    else:
        return [random.uniform(lower_list, upper_list)
                for _ in range(dimensions)]


#########################################
# Create Fitness and Individual Classes #
#########################################
creator.create("FitnessMin", base.Fitness, weights=(-1.0, -1.0, -1.0, -1.0))  # minimize objective functions
creator.create("Individual", list, fitness=creator.FitnessMin)

###############################################################
# Define operators and create individual and population types #
###############################################################
toolbox = base.Toolbox()
toolbox.register("uniformparams", uniform, LOWER, UPPER, IND_SIZE)
toolbox.register(
    "Individual",
    tools.initIterate,
    creator.Individual,
    toolbox.uniformparams)
toolbox.register("population", tools.initRepeat, list, toolbox.Individual)
toolbox.register("evaluate", evaluate)
toolbox.register(
    "mate",
    deap.tools.cxSimulatedBinaryBounded,  # binary crossover modifying the input individuals in-place
    eta=ETA,
    low=LOWER,
    up=UPPER)
toolbox.register("mutate", deap.tools.mutPolynomialBounded, eta=ETA,  # polynomial mutation (as in original NSGA-II)
                 low=LOWER, up=UPPER, indpb=0.1)  # indpb: independent probability for each attribute to be mutated
toolbox.register(
    "select",
    tools.selNSGA2)


##########################
# Optimization algorithm #
##########################
def main():
    par = [toolbox.evaluate([individualsToTest[subjectNumber,1],individualsToTest[subjectNumber,2]])]
    return par


if __name__ == '__main__':
    toolbox.register('map', futures.map)
    par = main()
    pickle.dump(par, open(filePath[-19:-4] + '_logbook_Test.pickle', 'wb'))