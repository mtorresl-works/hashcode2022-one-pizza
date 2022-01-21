from dataparser import *
from collections import *
import numpy as np

# inp: the input file as a single string
# out: the answer file produced by your solver, as a single string
# return the score of the output as an integer
def score(inp, out):
    ns = parse(inp)
    itr = (line for line in out.split('\n'))
    # TODO: implement
    pizzaChain = marina.outstring_to_pizza_chain(list(itr)[0], ns.NIng, ns.ingrList)
    score = marina.calc_score(ns.clients, pizzaChain)
    return score


