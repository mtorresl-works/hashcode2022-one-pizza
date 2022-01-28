import time
from ortools.sat.python import cp_model
import random

import utils.data_conversion as data_conversion
import utils.read_write as read_write

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

def solver_routine(graph):
    """Takes a graph as an input and returns the anticlique"""
    g = graph.copy()
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
    status = solver.Solve(model, solution_printer)

    print('Status = %s' % solver.StatusName(status))
    print('Number of solutions found: {:d}'.format(solution_printer.solution_count()))

    # Print solution.
    #if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:

    #vertices not in anticlique
    anticliqueComplement = [i for i in range(numVertex) if not solver.BooleanValue(x[i])]
    g.delete_vertices(anticliqueComplement)
    print("Estimation biggest anticlique: ", int(solver.BestObjectiveBound()))
    return g

def partition_graph(gAnticlique, gParent, nReturn=100):
    """Returns gAnticliqueKeep, gChild.
        gAnticliqueKeep is gAnticlique minus 100 random vertices
        gChild is gParent minus the 100 random vertices and their nearest neighbors.
        gAnticliqueKeep + any anticlique in gChild is an anticlique of gParent"""
    def flatten(t):
        return [item for sublist in t for item in sublist]

    gChild = gParent.copy()
    gAnticliqueKeep = gParent.copy()

    idsParent = set([c.id for c in gParent.vs['client_info']])
    idsAnticlique = set([c.id for c in gAnticlique.vs['client_info']])

    idsReturn = set(random.sample(idsAnticlique, nReturn))
    idsKeep = idsAnticlique - idsReturn

    neigh = flatten(gChild.neighborhood(vertices=gChild.vs[idsKeep], order=1, mode='all'))
    gChild.delete_vertices(neigh)
    gAnticliqueKeep.delete_vertices(idsParent - idsKeep)

    return gAnticliqueKeep, gChild

def merge_anticliques(gAnti1, gAnti2, gParent):
    gMerged = gParent.copy()

    idsParent = set([c.id for c in gParent.vs['client_info']])
    idsG1 = set([c.id for c in gAnti1.vs['client_info']])
    idsG2 = set([c.id for c in gAnti2.vs['client_info']])

    idsComplementary = idsParent - idsG1 - idsG2
    gMerged.delete_vertices(idsComplementary)

    return gMerged


if __name__ == '__main__':

    start_time = time.time()

    nMC = 1000
    nKeep = 400
    flags = data_conversion.read_flags()
    fId = flags.fId

    ns = data_conversion.create_client_ns(fId)

    gParent = read_write.read_graph(fId, anticlique=False, NVertex=flags.NV)
    gSolve = gParent.copy()

    gAnticlique = solver_routine(gSolve)
    bestScore = len(gAnticlique.vs)
    gAnticliqueBest = gAnticlique.copy()

    print("BEST score: {:d}".format(bestScore))
    #Dynamic improver...
    while True:
        nRemove = bestScore - nKeep

        gAnticliqueKeep, gChild = partition_graph(gAnticliqueBest, gParent, nRemove)
        gAnticliqueChild = solver_routine(gChild)
        print("Exited solver...")

        print("Best score: {:d}".format(bestScore))
        print("Kept Anticlique: ", len(gAnticliqueKeep.vs))
        print("New Anticlique: ", len(gAnticliqueChild.vs))

        newScore = len(gAnticliqueKeep.vs) + len(gAnticliqueChild.vs)
        print("New score: {:d}".format(newScore))
        if newScore > bestScore:
            print("NEW BEST")
            bestScore = newScore
            gAnticliqueBest = merge_anticliques(gAnticliqueKeep, gAnticliqueChild, gParent)
            if bestScore > 1790:
                read_write.export_graph(fId, gAnticliqueBest, anticlique=True)

    print("Vertices in anticlique: ", len(gAnticliqueBest.vs))
    read_write.export_graph(fId, gAnticliqueBest, anticlique=True)
