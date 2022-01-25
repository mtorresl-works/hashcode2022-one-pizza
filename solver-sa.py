import argparse
import random
from math import *
from copy import *
import time
import numpy as np

import data_conversion
"""
====== SOLVING ALGORITHM: SIMULATED ANNEALING ======
"""

def small_change(pizzaChain, NIngr, n=1):
    aux = copy(pizzaChain)
    flips = random.sample(range(NIngr), n)
    for k in flips:
        aux[k] = not(aux[k])
    return aux

def quot(beta, enerOld, enerNew, clients, C):
    exponent = -beta * (enerNew - enerOld)
    if exponent >= 0:
        Q = 1
    else:
        Q = exp(exponent)
    return Q


if __name__ == '__main__':

    start_time = time.time()

    flags = data_conversion.read_flags()

    inp = data_conversion.get_in_file_content(data_conversion.inputFiles[flags.fId])
    ns = data_conversion.parse(inp)

    score_to_energy = lambda score: (ns.C-score)

    print("# of clients: ", ns.C)
    print("# of ingredients: ", ns.NIng)


    p = 0.02 #maximum percentage of the chain to be change in a small change

    score, scoreBest, pizzaChainOld = data_conversion.gen_pizza_chain(flags.fId, flags.iC, ns.NIng, ns.clients)
    enerOld = score_to_energy(score)

    print('Best score so far: ', scoreBest)

    for i in range(flags.nMCgbl):
        acc = 0.0
        nFlips = flags.nFlips
        #round((nMC_global-i)/nMC_global * p*NIng)+1 #number of flips in a small change,decreases with i
        for j in range(flags.nMC):
            pizzaChainNew = small_change(pizzaChainOld, ns.NIng, nFlips)
            scoreNew = data_conversion.calc_score(ns.clients, pizzaChainNew)
            enerNew = score_to_energy(scoreNew)
            #print("Score: "+str(ener_to_score(enerNew)))
            if scoreNew > scoreBest: #keep track of the absolute minimum
                print("Best hit")
                scoreBest, pizzaChainBest = data_conversion.read_best(flags.fId) #scoreBest in file
                if scoreNew > scoreBest:
                    print("BEST HIT EVER: {:d}".format(scoreNew))
                    scoreBest, enerBest, pizzaChainBest = scoreNew, enerNew, copy(pizzaChainNew)
                    data_conversion.save_best(flags.fId, scoreBest, pizzaChainBest)

            if(quot(flags.beta, enerOld, enerNew, ns.clients, ns.C) > random.random()):
                #we accept
                enerOld = enerNew
                pizzaChainOld = copy(pizzaChainNew)
                acc += 1

        print("beta = {:.3f}, nFlips = {:d}, accept = {:.2f}, curr: {:d}, best: {:d} ({:.3f})".format(flags.beta, nFlips, acc/flags.nMC, scoreNew, scoreBest, scoreBest/ns.C))
        flags.beta += flags.deltaBeta
