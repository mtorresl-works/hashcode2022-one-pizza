import time
from ortools.sat.python import cp_model

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



if __name__ == '__main__':

    start_time = time.time()

    flags = data_conversion.read_flags()
    fId = flags.fId

    ### GRAPH DEFINITION
    g = read_write.read_graph(fId, anticlique=False, NVertex = int(flags.NV))

    edges = g.get_edgelist()
    numVertex = len(g.vs)
    if not numVertex == flags.NV:
        print("Warning:Read graph does not contain the specified number of vertices...")

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

    #vertices not in anticlique
    anticliqueComplement = [i for i in range(numVertex) if not solver.BooleanValue(x[i])]

    g.delete_vertices(anticliqueComplement)
    read_write.export_graph(fId, g, anticlique=True)

    print("Vertices in anticlique: ", len(g.vs))
    print("Estimation biggest anticlique: ", int(solver.BestObjectiveBound()))
