import argparse
import random
import sys
from collections import *
import numpy as np
from math import exp, ceil
import time
import marina
from copy import copy


"""
====== SOLVING ALGORITHM: ASEXUAL GENETIC ALGORITHM ======
"""
# TODO: clean up and add documentation

# These are the parameters you can play with
NRepeats = 50
initialMutRatio = 0.2
decay = 10


def gen_pop_init(NIng, initial_conditions=[]):
    if not initial_conditions.size == 0:
        return np.vstack(initial_conditions for i in range(flags.N1))
    else:
        return np.random.randint(2, size=(flags.N1, NIng))


# function for implementing the single-point crossover
def crossover(l, q, NIng):
    a, b = l.copy(), q.copy()
    # generating the random number to perform crossover
    k = np.random.randint(NIng)
    # interchanging the genes
    a[k:], b[k:] = q[k:].copy(), l[k:].copy()
    return a, b


def mutate(popSurvivals, scores, mu, NIng, N1, N2):
    """
    N1 number of parents
    N2 number of children per parent"""
    # weights = scores/np.sum(scores)
    # #Choosing the parents
    # random_parents = np.random.choice(range(N1), N1*N2, p=weights)
    #
    # #Crossover
    # children = np.zeros((N1*N2, NIng))
    # for i in range(N1*N2-1):
    #     children[i], children[i+1] = crossover(popSurvivals[random_parents[i]], popSurvivals[random_parents[i+1]], NIng)
    children = np.tile(popSurvivals, (N2,1)) #N2 copies along vertical axis

    #Mutate the children
    mutations = np.zeros((N1*N2, NIng))
    ones = np.ones((N1*N2, mu))
    random_ingr = np.random.choice(NIng, (N1*N2, mu))
    list(map(lambda mut, i: np.put(mut, random_ingr[i], ones), mutations, range(N1*N2)))
    return np.concatenate((popSurvivals, np.logical_xor(children,mutations)), axis=0)


def filter_by_score(scoresN1, population, clients, N1):
    """population is an np.array (dtype=object) of pizzaChains of size N1 + N1*N2.
    N1 is the size of the surviving population.
    The first N1 elements in population are the parents whose score is known (scoresN1)"""
    scores = scoresN1
    for pizzaChain in population[N1:]:
        s = marina.calc_score(clients, pizzaChain)
        scores.append(s)

    scores = np.array(scores)  # To be able to use arg sort
    idSorted = np.argsort(-scores)  # sort idx in ascending ording
    populationSorted = population[idSorted]
    scoresSorted = scores[idSorted]

    return populationSorted[:N1], list(scoresSorted[:N1])

if __name__ == '__main__':

    flags = marina.read_flags()

    inp = marina.get_in_file_content(marina.inputFiles[flags.fId])
    ns = marina.parse(inp)

    score, scoreBest, pizzaChain = marina.gen_pizza_chain(flags.fId, flags.iC, ns.NIng, ns.clients)

    print('Best score so far: ', scoreBest)

    if flags.iC = 'random':
        pizzaChain = []
    population = gen_pop_init(ns.NIng, initial_conditions=pizzaChain)

    scoresN1 = []
    for pizzaChain in population:
        s = marina.calc_score(ns.clients, pizzaChain)
        scoresN1.append(s)
    scoresN1 = np.array(scoresN1)  # To be able to use arg sort
    idSorted = np.argsort(-scoresN1)  # sort idx in ascending ording
    population = population[idSorted]
    scoresN1 = scoresN1[idSorted].tolist()

    counter = 0
    generation = 0
    while True:
        start_time = time.time()
        print("---Generation:" + str(generation))
        mu = ceil(ns.NIng * initialMutRatio * exp(-generation / decay))
        populationAugmented = mutate(population, scoresN1, mu, ns.NIng, flags.N1, flags.N2)
        population, scores = filter_by_score(scoresN1, populationAugmented, ns.clients, flags.N1)

        if scores[0] > scoreBest:
            print("Best hit")
            scoreBest, pizzaChainBest = marina.read_best(flags.fId)
            if scores[0] > scoreBest:
                print("BEST HIT EVER: {:d}".format(scores[0]))
                scoreBest, pizzaChainBest = scores[0], copy(population[0])
                marina.save_best(flags.fId, scoreBest, pizzaChainBest)

        print("Max score: {:d} ({:.3f})".format(scores[0], scores[0]/ns.C))
        if scoresN1[0] == scores[0]:
            counter += 1
        else:
            counter = 0

        if counter == NRepeats:
            break

        scoresN1 = scores
        generation += 1
        print("Execution time:" + str(time.time() - start_time))

    print("Final score:" + str(scores[0] / ns.C))
