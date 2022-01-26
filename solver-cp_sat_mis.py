import argparse
import time
import numpy as np

import igraph as ig
from ortools.linear_solver import pywraplp
from ortools.sat.python import cp_model

import marina

class VarArrayAndObjectiveSolutionPrinter(cp_model.CpSolverSolutionCallback):
  """Print intermediate solutions."""

  def __init__(self):
    cp_model.CpSolverSolutionCallback.__init__(self)
    self.__solution_count = 0

  def on_solution_callback(self):
    print('Solution %i' % self.__solution_count)
    print('  objective value = %i' % self.ObjectiveValue())
    print()
    self.__solution_count += 1

  def solution_count(self):
    return self.__solution_count



if __name__ == '__main__':

    start_time = time.time()

    flags = marina.read_flags()

    ### GRAPH DEFINITION
    g = marina.read_graph(flags.fId)
    edges = g.get_edgelist()
    numVertex = len(g.vs)

    ### SOLVER
    model = cp_model.CpModel()

    #Variables
    # x are the vertices (0 if not in MIS, 1 otherwise)
    x = [model.NewBoolVar('') for i in range(numVertex)] #we don't specifiy the name

    # Constraints
    for edge in edges:
        model.Add(sum([x[i] for i in edge]) <= 1)

    model.Maximize(sum(x))

    # Solve
    solver = cp_model.CpSolver()
    solution_printer = VarArrayAndObjectiveSolutionPrinter()
    status = solver.Solve(model,solution_printer)

    print('Status = %s' % solver.StatusName(status))
    print('Number of solutions found: {:d}'.format(solution_printer.solution_count()))

    # Print solution.
    #if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:

    anticlique = [i for i in range(numVertex) if solver.BooleanValue(x[i])]
    marina.save_anticlique(flags.fId, anticlique)

    mis = [g.vs[i]["client_info"] for i in range(numVertex) if solver.BooleanValue(x[i])]

    # pizzaChain = marina.optimal_pizza_chain(mis, ns.NIng)
    #
    # score = marina.calc_score(ns.clients, pizzaChain)
    # marina.save_ortools(flags.fId, score, pizzaChain)
    print("Final score: ", len(anticlique))
