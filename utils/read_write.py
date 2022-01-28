import numpy as np
import igraph as ig
from os import listdir, getcwd


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
    filename = './data_submissions/'+fId+'-submission_{:d}.out'.format(score)
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
    with np.load(filename) as data:
        return int(data['score']), data['pizzaChain']

def export_pizza(fId, score, method, pizzaChain):
    """
    Saves pizza chain
    :param fId: string indicating the file
    :param score: integer storing best score
    :param method: the solver routine type: greedy, mc, or
    :param pizzaChain: a binary array (0s and 1s) indicating the presence or absence of an ingredient in the solution
    """
    filename = './data_submissions/pizzas/'+fId+'-pizzaChain-'+method+'.npz'
    try:
        existentScore, pizzaDummy = read_pizza(fId, method)
        if existentScore < score:
            print("Best "+method+" hit")
            np.savez(filename, score=np.array(score), pizzaChain=pizzaChain)
    except:
        np.savez(filename, score=np.array(score), pizzaChain=pizzaChain)

def read_graph(fId, anticlique, NVertex=0):
    """
    Reads a binary file to a graph object
    :param fId: string indicating the file
    :param anticlique: boolean, are vertex disconnected or not?
    :param NVertex: # of vertices, in graph name. If not indicated, looks for the max available value.
    :return: a graph object
    """
    if anticlique:
        if NVertex:
            filename = './data_antigraphs/'+fId+'-anticlique-Nv_'+str(NVertex)+'.dat'
        else:
            fileList = listdir('./data_antigraphs/')
            fileListById = [x for x in fileList if fId + "-" in x]
            availableScores = [int(fn.split("_")[1]) for fn in [fp.split(".")[0] for fp in fileListById]]
            bestScore = max(availableScores)
            filename = './data_antigraphs/'+fId+'-anticlique-Nv_'+str(bestScore)+'.dat'
    else:
        fileList = listdir('./data_graphs_raw/')
        filename = './data_graphs_raw/' + [x for x in fileList if fId+"-" in x][0]
        filename = './data_graphs_raw/'+fId+'-Nv_'+str(NVertex)+'.dat'

    graph = ig.read(filename, format='pickle')
    return graph

def export_graph(fId, graph, anticlique):
    """
    Prints a graph object to a binary file
    :param fId: string indicating the file
    :param graph: a graph object
    :param anticlique: boolean, are vertex disconnected or not?
    """
    NVertex = len(graph.vs)
    if anticlique:
        filename = './data_antigraphs/'+fId+'-anticlique-Nv_'+str(NVertex)+'.dat'
    else:
        filename = './data_graphs_raw/'+fId+'-Nv_'+str(NVertex)+'.dat'

    graph.write(filename, format='pickle')
