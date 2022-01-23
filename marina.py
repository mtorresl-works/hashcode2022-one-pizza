import numpy as np
import igraph
from itertools import combinations
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse
"""
====== OBJECT DEFINITION ======
"""


class Client:
    def __init__(self, likes, dislikes):
        """likes and dislikes are lists of strings read from file"""
        self.id = 0
        self.L = int(likes[0])  # number of ingredients client likes
        self.D = int(dislikes[0])  # number of ingredients client dislikes
        self.l_ingr_s = likes[1:] # likes as a list of strings
        self.d_ingr_s = dislikes[1:] # dislikes as a list of strings
        self.l_ingr = {} # likes as a set of indexes
        self.d_ingr = {} # dislikes as a set of indexes

    #
    def set_indexes(self, clients, ingrList):
        """
        Given a list of ingredients, sets the clients' preferences as two sets of indexes to access ingrList.
        Also sets the client index inside the list of clietns
        :param clients: the list containing all the clients
        :param ingrList: a list of strings
        :return: void
        """
        self.id = clients.index(self)
        self.l_ingr = {ingrList.index(item) for item in self.l_ingr_s}
        self.d_ingr = {ingrList.index(item) for item in self.d_ingr_s}

    def is_coming(self, pizzaChain):
        """
        Returns True if client gives points, False otherwise.
        :param pizzaChain: a binary array (0s and 1s) indicating the presence or absence of an ingredient in the solution
        :return: a boolean
        """
        ingrSet = set(np.argwhere(pizzaChain == 1).flatten())
        if not self.l_ingr.issubset(ingrSet) or self.d_ingr.intersection(ingrSet):
            return False
        else:
            return True

    def print_client(self):
        print(self.L)
        print(self.l_ingr_s)
        print(self.D)
        print(self.d_ingr_s)


def gen_ingr(clients):
    """
    Creates the complete list of ingredients.
    :param clients: the list containing all the clients
    :return: a list of strings
    """
    ingrList = []
    for c in clients:
        ingrList += c.l_ingr_s
        ingrList += c.d_ingr_s

    return list((dict.fromkeys((ingrList)))) #sets don't preserve order. Use dict instead!


def update_indexes(clients, ingrList):
    """
    Updates l_ingr and d_ingr of each client given a complete list of ingredients.
    :param clients: the list containing all the clients
    :param ingrList: a list of strings
    :return: void
    """
    for client in clients:
        client.set_indexes(clients,ingrList)


"""
====== FILE PROCESSING ======
"""

inputFiles = {'a': "./input_data/a_an_example.in",\
              'b': "./input_data/b_basic.in",\
              'c': "./input_data/c_coarse.in",\
              'd': "./input_data/d_difficult.in",\
              'e': "./input_data/e_elaborate.in"}

def get_in_file_content(filename):
    """
    Reads file contents and transforms it in a string
    """
    try:
        with open(filename) as f:
            return f.read()
    except:
        print("Error opening file "+filename)
        return -1


def parse(inp):
    """
    Generates namespace with relevant variables from string.
    To be called from solver and submission_generator
    """
    ns = argparse.Namespace()
    ns.C, ns.clients = read_single_line_input(inp)
    ns.ingrList = gen_ingr(ns.clients)
    ns.NIng = len(ns.ingrList)
    update_indexes(ns.clients, ns.ingrList)

    return ns


def read_single_line_input(filestring):
    """
    Parses the input file content to the list of clients.
    :param filestring: the input file content in one line
    :return: a tuple containing the number of clients and a preliminary list of clients only with l_ingr_s and d_ingr_s
    """
    data = filestring.split('\n')
    C = int(data[0])
    clients = []
    for cL, cD in zip(data[1::2], data[2::2]):
        cL = cL.split(' ')  # split in an array of words
        cD = cD.split(' ')
        clients.append(Client(cL, cD))

    return C, clients


def pizza_chain_to_outstring(pizzaChain, NIng, ingrList):
    """
    Parses the binary array to the output file content.
    :param pizzaChain:  a binary array (0s and 1s) indicating the presence or absence of an ingredient in the solution
    :param NIng: the number of ingredients
    :param ingrList: a list of strings with all the ingredients.
    :return: the output file content in one line
    """
    otr = str(sum(pizzaChain))
    for idx, spin in enumerate(pizzaChain):  # idx position in chain, spin True or False
        if spin: otr = otr + ' ' + ingrList[idx]
    return otr + "\n"


def read_best(fId):
    """
    Returns best config ever
    :fId: string indicating the file
    returns score, pizzaChain
    """
    filename = 'best_runs/'+fId+'-best_pizzaChain.npz'
    try:
        with np.load(filename) as data:
            return int(data['score']), data['pizzaChain']
    except:
        print("Error: couldn't open "+filename)
        print("Best score set to 0")
        return 0, None


def save_best(fId, score, pizzaChain):
        """
        Saves pizza chain
        :fId: string indicating the file
        :score: integer storing best score
        """
        filename = 'best_runs/'+fId+'-best_pizzaChain.npz'
        np.savez(filename, score=np.array(score), pizzaChain=pizzaChain)


def print_best_score(fId):
        """
        Prints best score ever
        :fId: string indicating the file
        """
        filename = 'best_runs/'+fId+'-best_pizzaChain.npz'
        try:
            with np.load(filename) as data:
                print("Best score ever for file "+fId+": {:d}".format(int(data['score'])))

        except:
            print("Error: couldn't open "+filename)
            print("Best score is 0")


def print_submission_file(fId, ingrList, score, pizzaChain):
    """
    Converts the binary solution to the output string and prints it to a file.
    (WARNING: not used in the final version of the code, only for the example in this script).
    :param filenameOut: the name of the output file.
    :param ingrList: a list of strings with all the ingredients.
    :param pizzaChain: a binary array (0s and 1s) indicating the presence or absence of an ingredient in the solution
    :return: void
    """
    filename = './output_data/'+fId+'-score_{:d}.out'.format(score)
    N = sum(pizzaChain)
    with open(filename, 'w') as f:
        f.write(pizza_chain_to_outstring(pizzaChain, N, ingrList))
    f.close()


"""
====== SCORING ======
"""

def calc_score(clients, pizzaChain):
    """
    Calculates the score of a trial solution given a list of clients.
    :param clients: the list containing all the clients
    :param pizzaChain: a binary array (0s and 1s) indicating the presence or absence of an ingredient in the solution
    :return:
    """
    score = 0
    for client in clients:
        if client.is_coming(pizzaChain):
            score = score + 1
    return score

"""
====== RANDOM INITIALIZERS======
"""

def gen_pizza_chain_random(NIng):
    pizzaChain = np.random.choice([0,1], size = NIng)
    return pizzaChain

"""
====== MAXIMUM INDEPENDENT SET ======
To find optimal initial conditions
"""
def check_compatibility(two_clients, edgeList):
    index0 = two_clients[0].id
    index1 = two_clients[1].id
    # if not (index0 % 100) and index1 == index0 + 1:
    #     print("Checking clients "+str(index0)+" and "+str(index1))
    if two_clients[0].l_ingr.intersection(two_clients[1].d_ingr) or two_clients[1].l_ingr.intersection(
            two_clients[0].d_ingr):
        edgeList.append((index0, index1))

def create_graph(clients):
    print("Creating client network...")
    g = igraph.Graph()
    g.add_vertices(len(clients))
    g.vs["client_info"] = clients
    edgeList = []
    for two_clients in combinations(clients, 2):
        check_compatibility(two_clients, edgeList)
    g.add_edges(edgeList)
    print("Done! Vertex = "+str(g.vcount())+" Edges = "+str(g.ecount()))
    return g

def largest_clients_group(g):
    print("Calculating the largest independent set of clients...")
    indSet = []
    # independentSet = igraph.GraphBase.largest_independent_vertex_sets(g)[0]
    while g.vcount():
        degree = 0
        vSequence = g.vs.select(_degree=degree)
        while not len(vSequence):
            degree = degree + 1
            vSequence = g.vs.select(_degree=degree)
        # print("degree = " + str(degree))
        v = vSequence[0]
        indSet.append(v['client_info'])
        nSequence = g.neighbors(v, mode='all')
        g.delete_vertices(nSequence)
        g.delete_vertices([v])
    print("Done! Initial score = "+str(len(indSet)))
    return indSet

def optimal_pizza_chain(indClients, NIng):
    commonLikesIndex = [client.l_ingr for client in indClients]
    activeIngr = list(set().union(*commonLikesIndex))
    pizzaChain = np.zeros(NIng)
    pizzaChain[activeIngr] = 1
    return pizzaChain

def starting_config_routine(clients, NIng):
    graph = create_graph(clients)
    indSet = largest_clients_group(graph)
    return optimal_pizza_chain(indSet, NIng)
