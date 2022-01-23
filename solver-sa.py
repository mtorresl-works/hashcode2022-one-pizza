import argparse
import random
from math import *
from copy import *
import time
import numpy as np

import marina
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


def read_flags(fId, iC, nMC, nMCgbl, deltaBeta):

        parser = argparse.ArgumentParser()

        parser.add_argument('-fId', help="Input file identifier (str). Default = "+fId, type=str, default=fId)
        parser.add_argument('-iC', help="Initial configuration (str). 'random' or 'best'. Default = "+iC, type=str, default=iC)
        parser.add_argument('-nMC', help="Minibatch # of iterations (int). Default = "+str(nMC), type=int, default=nMC)
        parser.add_argument('-nMCgbl', help="Bigbatch # of iterations (int). Default = "+str(nMCgbl), type=int, default=nMCgbl)
        parser.add_argument('-deltaBeta', help="Step in beta (float). Default = "+str(deltaBeta), type=float, default=deltaBeta)

        return parser.parse_args()

if __name__ == '__main__':

    start_time = time.time()

    flags = read_flags(fId='a', iC='random', nMC=100, nMCgbl=20, deltaBeta=0.02)

    inp = marina.get_in_file_content(marina.inputFiles[flags.fId])
    ns = marina.parse(inp)

    score_to_energy = lambda score: (ns.C-score)

    print("# of clients: ", ns.C)
    print("# of ingredients: ", ns.NIng)

    beta = abs(100/ns.C)
    p = 0.02 #maximum percentage of the chain to be change in a small change

    if flags.iC == 'random':
        pizzaChainOld = marina.gen_pizza_chain_random(ns.NIng)#random
        scoreOld = marina.calc_score(ns.clients, pizzaChainOld)
        enerOld = score_to_energy(scoreOld)

        scoreBest, pizzaChainBest = marina.read_best(flags.fId)

        if scoreOld > scoreBest:
            scoreBest, enerBest, pizzaChainBest = scoreOld, enerOld, copy(pizzaChainOld)
            marina.save_best(flags.fId, scoreBest, pizzaChainBest)

    elif flags.iC == 'best':
        scoreBest, pizzaChainBest = marina.read_best(flags.fId)
        enerBest = score_to_energy(scoreBest)
        scoreOld, enerOld, pizzaChainOld = scoreBest, enerBest, copy(pizzaChainBest)

    print('Best score so far: ', scoreBest)

    for i in range(flags.nMCgbl):
        acc = 0.0
        nFlips =5# round((nMC_global-i)/nMC_global * p*NIng)+1 #number of flips in a small change,decreases with i
        for j in range(flags.nMC):
            pizzaChainNew = small_change(pizzaChainOld, ns.NIng, nFlips)
            scoreNew = marina.calc_score(ns.clients, pizzaChainNew)
            enerNew = score_to_energy(scoreNew)
            #print("Score: "+str(ener_to_score(enerNew)))
            if scoreNew > scoreBest: #keep track of the absolute minimum
                print("Best hit")
                scoreBest, pizzaChainBest = marina.read_best(flags.fId) #scoreBest in file
                if scoreNew > scoreBest:
                    print("BEST HIT EVER: {:d}".format(scoreNew))
                    scoreBest, enerBest, pizzaChainBest = scoreNew, enerNew, copy(pizzaChainNew)
                    marina.save_best(flags.fId, scoreBest, pizzaChainBest)

            if(quot(beta, enerOld, enerNew, ns.clients, ns.C) > random.random()):
                #we accept
                enerOld = enerNew
                pizzaChainOld = copy(pizzaChainNew)
                acc += 1

        print("beta = {:.3f}, nFlips = {:d}, accept = {:.2f}, best : {:d} ({:.3f})".format(beta, nFlips, acc/flags.nMC, scoreBest, scoreBest/ns.C))
        beta += flags.deltaBeta
