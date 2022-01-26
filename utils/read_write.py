import numpy as np
import igraph as ig


def input_file_to_string(filename):
    """
    Reads file contents and transforms it in a string.
    :param filename: a string containing the name of the file
    :return: the file content as a string
    """
    try:
        with open(filename) as f:
            return f.read()
    except:
        print("Error opening file "+filename)
        return -1

def string_to_submission_file(oStr, fId, score):
    '''
    Prints the solution string to a submission file
    :param oStr: string variable with the file content
    :param fId: string indicating the (input example) file ID
    :param score: integer storing best score
    '''
    filename = './data_submissions/'+fId+'-score_{:d}.out'.format(score)
    with open(filename, 'w') as f:
        f.write(oStr)
    f.close()

def read_pizza(fId, method):
    """
    return a pizza config
    :fId: string indicating the file
    :method: greedy, mc, or
    :return: score, pizzaChain
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
    :param fId: string indicating the file
    :param score: integer storing best score
    :param method: the solver routine type: greedy, mc, or
    :param pizzaChain: a binary array (0s and 1s) indicating the presence or absence of an ingredient in the solution
    """
    filename = './data_submissions/pizzas/'+fId+'-pizzaChain-'+method+'.npz'
    np.savez(filename, score=np.array(score), pizzaChain=pizzaChain)

def read_graph(fId, folder):
    """
    Reads a binary file to a grahp object
    :param fId: string indicating the file
    :folder: data_graphs_raw or data_antigraphs
    :return: a graph object

    """
    filename = './'+folder+'/'+fId+'.dat'
    graph = ig.read(filename, format='pickle')
    return graph

def export_graph(fId, graph, folder):
    """
    Prints a graph object to a binary file
    :fId: string indicating the file
    :folder: data_graphs_raw or data_antigraphs
    :param graph: a graph object
    """
    filename = './'+folder+'/'+fId+'.dat'
    graph.write(filename, format='pickle')


def export_graph_raw(fId, graph):
    """
    Prints a graph object to a binary file
    :fId: string indicating the file
    :param graph: a graph object
    """
    filename = './data_graphs_raw/'+fId+'.dat'
    graph.write(filename, format='pickle')
