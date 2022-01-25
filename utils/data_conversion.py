import numpy as np
import igraph as ig
import argparse

import clients
import read_write

inputFiles = {'a': "./data_input/a_an_example.in",\
              'b': "./data_input/b_basic.in",\
              'c': "./data_input/c_coarse.in",\
              'd': "./data_input/d_difficult.in",\
              'e': "./data_input/e_elaborate.in"}


def read_flags(fId='a', iC='random', nMC=100, nMCgbl=100, beta=0.01, deltaBeta=0.005, nFlips=5, N1=5, N2=2):
    """Reads flags for all solvers"""

        parser = argparse.ArgumentParser()

        """ ALL SOLVERS """

        parser.add_argument('-fId', help="Input file identifier (str). Default = "+fId, type=str, default=fId)
        parser.add_argument('-iC', help="Initial configuration (str). 'random', 'best' or 'greedy'. Default = "+iC, type=str, default=iC)

        """ SA SOLVER """

        parser.add_argument('-nMC', help="(SA) Minibatch # of iterations (int). Default = "+str(nMC), type=int, default=nMC)
        parser.add_argument('-nMCgbl', help="(SA) Bigbatch # of iterations (int). Default = "+str(nMCgbl), type=int, default=nMCgbl)
        parser.add_argument('-beta', help="(SA) Initial beta (float). Default = "+str(beta), type=float, default=beta)
        parser.add_argument('-deltaBeta', help="(SA) Step in beta (float). Default = "+str(deltaBeta), type=float, default=deltaBeta)
        parser.add_argument('-nFlips', help="(SA) Flips # in small change (int). Default = "+str(nFlips), type=int, default=nFlips)

        """ AGA SOLVER """
        parser.add_argument('-N1', help="(AGA) # of parents (int). Default = "+str(N1), type=int, default=N1)
        parser.add_argument('-N2', help="(AGA) # of children per parent (int). Default = "+str(N2), type=int, default=N2)


        return parser.parse_args()


def input_string_to_clients(filestring):
    """
    Parses the input file content to the list of clients.
    :param filestring: the input file content in one string
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


def create_client_ns(fId):
    """
    Generates namespace with relevant variables.
    To be called from solver and submission_generator
    """
    inp = read_and_write.input_file_to_string(inputFiles[fId])
    ns = argparse.Namespace()
    ns.C, ns.clients = input_string_to_clients(inp) #see function above
    ns.ingrList = clients.cs_to_ingr_list(ns.clients)
    ns.NIng = len(ns.ingrList)
    clients.update_indexes(ns.clients, ns.ingrList)

    return ns


def pizzaChain_to_outstring(pizzaChain, NIng, ingrList):
    """
    Parses the binary array to the output file content.
    :param pizzaChain:  a binary array (0s and 1s) indicating the presence or absence of an ingredient in the solution
    :param NIng: the number of ingredients
    :param ingrList: a list of strings with all the ingredients.
    :return: the output file content in one line
    """
    otr = str(int(sum(pizzaChain)))
    for idx, spin in enumerate(pizzaChain):  # idx position in chain, spin True or False
        if spin: otr = otr + ' ' + ingrList[idx]
    return otr + "\n"


def graph_to_pizza(graph, NIng):
    """
    Creates a pizza (np.array of 0s and 1s of length Number of Ingredients)
    from a graph object.
    Vertex in graph have the attribute of client
    """
    commonLikesIndex = [client.l_ingr for client in graph.vs['client_info']]
    activeIngr = list(set().union(*commonLikesIndex))
    pizzaChain = np.zeros(NIng)
    pizzaChain[activeIngr] = 1
    return pizzaChain


def clients_to_graph(cs):
    """Creates graph object from client list"""
    
    def check_compatibility(two_cs, edgeList):
        index0 = two_cs[0].id
        index1 = two_cs[1].id
        # if not (index0 % 100) and index1 == index0 + 1:
        #     print("Checking clients "+str(index0)+" and "+str(index1))
        if set(two_cs[0].l_ingr).intersection(set(two_cs[1].d_ingr)) or set(two_cs[1].l_ingr).intersection(
                set(two_cs[0].d_ingr)):
            edgeList.append((index0, index1))

    print("Creating client network...")
    g = ig.Graph()
    g.add_vertices(len(cs))
    g.vs["client_info"] = cs
    edgeList = []
    for two_cs in combinations(cs, 2):
        check_compatibility(two_cs, edgeList)
    g.add_edges(edgeList)
    print("Done! Vertex = "+str(g.vcount())+" Edges = "+str(g.ecount()))
    return g
