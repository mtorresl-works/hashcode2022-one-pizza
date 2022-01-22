import argparse
import random
import sys
sys.path.extend(['..', '.'])
from collections import *
from dataparser import parse
from util import get_in_file_content
from custom import marina
from math import *
from copy import *
import time
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

def gen_pop_init(NIng, flag, fId = 0, Nc =0):
    if flag == 0: #all 1s
        pizzaChain = np.ones(NIng)
    # elif flag == 1: #from file
    #     sizes = ["a", "b", "c", "d", "e"]
    #     fName = "best_config/"+sizes[fId]+"_Nc_"+str(Nc)+".dat"
    #     with open(fName, 'r') as f:
    #         data = f.readlines()
    #         pizzaChain = [int(spin) for spin in data[0]]
    #     f.close()
    else:
        pizzaChain = np.random.choice([0,1], size(NIngr))
    return pizzaChain

# inp is an input file as a single string
# return your output as a string
def solve(inp, args):
    start_time = time.time()
    random.seed(args['seed'])
    ns = parse(inp)
    fId=0
    score_to_energy = lambda score: (C-score)

    print("# of clients: ", ns.C)
    print("# of ingredients: ", ns.NIng)

    nMC_Vals = [100,200,500,500,1000]
    nMC_Global_Vals = [10,20,50,100,50]
    beta = abs(100/ns.C)
    deltaBeta = 0.02
    p = 0.02 #maximum percentage of the chain to be change in a small change

    pizzaChainOld = gen_pop_init(ns.NIng, flag=flag, fId=fId, Nc =prevScore)#0 all 1s, 1 file, else random
    enerOld = score_to_energy(marina.calc_score(ns.clients, pizzaChainOld))

    enerBest = enerOld
    pizzaChainBest = copy(pizzaChainOld)
    print(ns.C-enerBest)
    #print_file(fId, ingrSet, pizzaChainBest, ener_to_score(enerBest))

    nMC_global = nMC_Global_Vals[fId]
    nMC = nMC_Vals[fId]

    for i in range(nMC_global):
        acc = 0.0
        nFlips =3# round((nMC_global-i)/nMC_global * p*NIng)+1 #number of flips in a small change,decreases with i
        for j in range(nMC):
            pizzaChainNew = small_change(pizzaChainOld, ns.NIng, nFlips)
            enerNew = score_to_energy(marina.calc_score(ns.clients, pizzaChainNew))
            #print("Score: "+str(ener_to_score(enerNew)))
            if enerNew < enerBest: #keep track of the absolute minimum
                enerBest = enerNew
                pizzaChainBest = copy(pizzaChainNew)
                #print_file(fId, ingrSet, pizzaChainBest, ener_to_score(enerBest))
                print("BEST HIT")
            if(quot(beta, enerOld, enerNew, clients, C) > random.random()):
                #we accept
                enerOld = enerNew
                pizzaChainOld = copy(pizzaChainNew)
                acc += 1

        print("beta = {:.3f}, nFlips = {:d}, accept = {:.2f}, best : {:d} ({:.3f})".format(beta, nFlips, acc/nMC, ns.C - enerBest, (ns.C-enerBest)/ns.C))
        beta += deltaBeta

    #print("# of clients: {:d}, score: {:.2f}".format(C-enerBest,(C-enerBest)/C))
    #print_file(filenames[fId][:-7]+"-Nc_{:d}.out".format(C-enerBest), ingrSet, pizzaChainBest)



    end_time = time.time()
    print("Execution time: ", end_time-start_time)

    return marina.pizza_chain_to_outstring(pizzaChainBest, ns.NIng, ns.ingrList)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('in_file')
    args = parser.parse_args()
    inp = get_in_file_content(args.in_file)
    out = solve(inp, {'seed': 0})
    print('\n'.join(['OUT:', '=========', out]))
