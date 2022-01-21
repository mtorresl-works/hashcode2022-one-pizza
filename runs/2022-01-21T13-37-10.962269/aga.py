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


# inp is an input file as a single string
# return your output as a string
def solve(inp, args):
    time_init = time()
    # TODO: Solve the problem
    random.seed(args['seed'])
    ns = parse(inp)

    # These are the parameters you can play with
    NRepeats = 50
    N1 = 4  # total of survivals
    N2 = 2  # number of descendants per survival
    initialMutRatio = 0.2
    decay = 200

    # Initial population
    population = marina.gen_pop_init(N1, ns.NIng)
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
        populationAugmented = marina.mutate(population, scoresN1, mu, ns.NIng, N1, N2)
        population, scores = marina.filter_by_score(N1, scoresN1, populationAugmented, ns.clients)

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
