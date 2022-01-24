import argparse
import time
import numpy as np

import igraph as ig
from ortools.linear_solver import pywraplp

import marina

if __name__ == '__main__':

    start_time = time.time()

    flags = marina.read_flags()

    inp = marina.get_in_file_content(marina.inputFiles[flags.fId])
    ns = marina.parse(inp)

    ### GRAPH DEFINITION
    g = marina.create_graph(ns.clients)
    edges = g.get_edgelist()
    numVertex = ns.C

    ### SOLVER
    solver = pywraplp.Solver.CreateSolver('SCIP')


    # x are the vertices (0 if not in MIS, 1 otherwise)
    x = {}
    for i in range(numVertex):
        x[i] = solver.IntVar(0, 1, '')

    # Constraints
    for edge in edges:
        solver.Add(solver.Sum([x[i] for i in edge]) <= 1)

    solver.Maximize(solver.Sum([x[i] for i in range(numVertex)]))

    # Solve
    status = solver.Solve()

    # Print solution.
    mis = [g.vs[i]["client_info"] for i in range(numVertex) if x[i].solution_value() > 0.5]

    pizzaChain = marina.optimal_pizza_chain(mis, ns.NIng)

    score = marina.calc_score(ns.clients, pizzaChain)
    marina.save_ortools(flags.fId, score, pizzaChain)
    print("Final score: ", score)
