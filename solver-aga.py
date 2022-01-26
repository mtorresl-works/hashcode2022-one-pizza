import numpy as np
from math import exp, ceil
import time
from copy import copy

import utils.data_conversion as data_conversion
import utils.read_write as read_write
import utils.scorer as scorer


"""
====== SOLVING ALGORITHM: ASEXUAL GENETIC ALGORITHM ======
"""
# TODO: clean up and add documentation

# These are the parameters you can play with
# NRepeats = 50
initialMutRatio = 0.2
decay = 10


def gen_pop_init(NIng, initial_conditions=[]):
    if not initial_conditions.size == 0:
        return np.vstack([initial_conditions]+list(np.random.randint(2, size=(flags.N1-1, NIng))))
    else:
        return np.random.randint(2, size=(flags.N1, NIng))


def mutate(popSurvivals, scores, mu, NIng, N1, N2):
    """
    N1 number of parents
    N2 number of children per parent"""
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
        s = scorer.score_from_pizza(clients, pizzaChain)
        scores.append(s)

    scores = np.array(scores)  # To be able to use arg sort
    idSorted = np.argsort(-scores)  # sort idx in ascending ording
    populationSorted = population[idSorted]
    scoresSorted = scores[idSorted]

    return populationSorted[:N1], list(scoresSorted[:N1])

if __name__ == '__main__':

    flags = data_conversion.read_flags()
    ns = data_conversion.create_client_ns(flags.fId)

    try:
        scoreBest, pizzaChainBest = read_write.read_pizza(flags.fId, "mc")
        print('Best score so far: ', scoreBest)
    except:
        pizzaChainBest = np.array([])

    # pizzaChainBest = np.array([]) # Use this if you want N1 different random individuals, instead of N1 pizzaChain clones
    population = gen_pop_init(ns.NIng, initial_conditions=pizzaChainBest)

    scoresN1 = []
    for pizzaChain in population:
        s = scorer.score_from_pizza(ns.clients, pizzaChain)
        scoresN1.append(s)
    scoresN1 = np.array(scoresN1)  # To be able to use arg sort
    idSorted = np.argsort(-scoresN1)  # sort idx in ascending ording
    population = population[idSorted]
    scoresN1 = scoresN1[idSorted].tolist()

    counter = 0
    generation = 0
    start_time = time.time()
    try:
        while True:
            print("---Generation:" + str(generation))
            mu = ceil(ns.NIng * initialMutRatio * exp(-generation / decay))
            populationAugmented = mutate(population, scoresN1, mu, ns.NIng, flags.N1, flags.N2)
            population, scores = filter_by_score(scoresN1, populationAugmented, ns.clients, flags.N1)

            read_write.export_pizza(flags.fId, scores[0], "mc", copy(population[0]))

            print("Max score: {:d} ({:.3f})".format(scores[0], scores[0]/ns.C))
            if scoresN1[0] == scores[0]:
                counter += 1
            else:
                counter = 0

            # if counter == NRepeats:
            #     break

            scoresN1 = scores
            generation += 1
            print("Execution time:" + str(time.time() - start_time))

    except KeyboardInterrupt:
        print("Final score:" + str(scores[0] / ns.C))
        pass
