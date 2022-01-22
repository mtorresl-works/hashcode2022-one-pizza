import argparse
import random
import sys
sys.path.extend(['..', '.'])
from collections import *
from dataparser import parse
from util import get_in_file_content
import numpy as np
from math import exp, ceil
from time import time

from custom import marina


"""
====== SOLVING ALGORITHM: ASEXUAL GENETIC ALGORITHM ======
"""
# TODO: clean up and add documentation

# These are the parameters you can play with
NRepeats = 50
N1 = 3  # total of survivals
N2 = 2  # number of descendants per survival
initialMutRatio = 0.2
decay = 10


def gen_pop_init(NIng, initial_conditions=[]):
    if not initial_conditions.size == 0:
        return np.vstack((initial_conditions for i in range(N1)))
    else:
        return np.random.randint(2, size=(N1, NIng))


# function for implementing the single-point crossover
def crossover(l, q, NIng):
    a, b = l.copy(), q.copy()
    # generating the random number to perform crossover
    k = np.random.randint(NIng)
    # interchanging the genes
    a[k:], b[k:] = q[k:].copy(), l[k:].copy()
    return a, b


def mutate(popSurvivals, scores, mu, NIng):
    # weights = scores/np.sum(scores)
    # #Choosing the parents
    # random_parents = np.random.choice(range(N1), N1*N2, p=weights)
    #
    # #Crossover
    # children = np.zeros((N1*N2, NIng))
    # for i in range(N1*N2-1):
    #     children[i], children[i+1] = crossover(popSurvivals[random_parents[i]], popSurvivals[random_parents[i+1]], NIng)
    children = np.tile(popSurvivals, (N2,1))

    #Mutate the children
    mutations = np.zeros((N1*N2, NIng))
    ones = np.ones((N1*N2, mu))
    random_ingr = np.random.choice(NIng, (N1*N2, mu))
    list(map(lambda mut, i: np.put(mut, random_ingr[i], ones), mutations, range(N1*N2)))
    return np.concatenate((popSurvivals, np.logical_xor(children,mutations)), axis=0)


def filter_by_score(scoresN1, population, clients):
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


# inp is an input file as a single string
# return your output as a string
def solve(inp, args):
    time_init = time()
    random.seed(args['seed'])
    ns = parse(inp)
    pizzaChain = marina.starting_config_routine(ns.clients, ns.NIng)

    # Initial population
    population = gen_pop_init(ns.NIng, initial_conditions = pizzaChain)
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
        print("---Generetion:" + str(generation))
        mu = ceil(ns.NIng * initialMutRatio * exp(-generation / decay))
        populationAugmented = mutate(population, scoresN1, mu, ns.NIng)
        population, scores = filter_by_score(scoresN1, populationAugmented, ns.clients)

        print("Max score:" + str(scores[0]))
        if scoresN1[0] == scores[0]:
            counter += 1
        else:
            counter = 0

        if counter == NRepeats:
            break

        scoresN1 = scores
        generation += 1
        print("Execution time:" + str(time() - time_init))

    print("Final score:" + str(scores[0] / ns.C))

    return marina.pizza_chain_to_outstring(population[0], ns.NIng, ns.ingrList)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('in_file')
    args = parser.parse_args()
    inp = get_in_file_content(args.in_file)
    out = solve(inp, {'seed': 0})
    print('\n'.join(['OUT:', '=========', out]))
