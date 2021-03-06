import argparse
import time
import numpy as np

import igraph as ig
from ortools.linear_solver import pywraplp

import utils.data_conversion as data_conversion
import utils.scorer as scorer
import utils.read_write as read_write

if __name__ == '__main__':

    start_time = time.time()

    flags = data_conversion.read_flags()

    ns = data_conversion.create_client_ns(flags.fId)

    ### GRAPH DEFINITION
    try:
        g = read_write.read_graph(flags.fId, False)
    except:
        g = data_conversion.clients_to_graph(ns.clients)
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
    gsolved = g.copy()
    anti_mis = [g.vs[i] for i in range(numVertex) if x[i].solution_value() < 0.5]
    gsolved.delete_vertices(anti_mis)


    pizzaChain = data_conversion.graph_to_pizza(gsolved, ns.NIng)

    score = scorer.score_from_graph(gsolved)
    read_write.export_graph(flags.fId, gsolved, True)
    read_write.export_pizza(flags.fId, score, "or", pizzaChain)
    print("Final score: ", score)
