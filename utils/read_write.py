import numpy as np
import igraph as ig


def input_file_to_string(filename):
    """
    Reads file contents and transforms it in a string
    """
    try:
        with open(filename) as f:
            return f.read()
    except:
        print("Error opening file "+filename)
        return -1

def string_to_submission_file(oStr, fId, score):
    filename = './data_submissions/'+fId+'-score_{:d}.out'.format(score)
    with open(filename, 'w') as f:
        f.write(oStr)
    f.close()

def read_pizza(fId, method):
    """
    Returns a pizza config
    :fId: string indicating the file
    :method: greedy, mc, or
    returns score, pizzaChain
    """
    filename = './data_submissions/pizzas/'+fId+'-pizzaChain-'+method+'.npz'
    try:
        with np.load(filename) as data:
            return int(data['score']), data['pizzaChain']
    except:
        print("Error: couldn't open "+filename)
        print("Best score set to 0")
        return 0, None

def export_pizza(fId, score, method, pizzaChain):
    """
    Saves pizza chain
    :fId: string indicating the file
    :method: greedy, mc, or
    :score: integer storing best score
    """
    filename = './data_submissions/pizzas/'+fId+'-pizzaChain-'+method+'.npz'
    np.savez(filename, score=np.array(score), pizzaChain=pizzaChain)

def read_graph(fId):
        """
        Returns a grahp object
        :fId: string indicating the file
        """
        filename = 'data_graphs_raw/'+fId+'.dat'
        graph = ig.read(filename, format='pickle')
        return graph

def export_graph(fId, graph):
        """
        Saves graphs to open with different solvers
        """
        filename = './data_graphs_raw/'+fId+'.dat'
        graph.write(filename, format='pickle')
