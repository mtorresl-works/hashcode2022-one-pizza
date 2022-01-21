from math import *
import numpy as np
from time import time


"""
====== OBJECT DEFINITION ======
"""


class Client:
    def __init__(self, likes, dislikes):
        """likes and dislikes are lists of strings read from file"""
        self.L = int(likes[0])  # number of ingredients client likes
        self.D = int(dislikes[0])  # number of ingredients client dislikes
        self.l_ingr_s = likes[1:] # likes as a list of strings
        self.d_ingr_s = dislikes[1:] # dislikes as a list of strings
        self.l_ingr = {} # likes as a set of indexes
        self.d_ingr = {} # dislikes as a set of indexes

    #
    def set_indexes(self, ingrList):
        """
        Given a list of ingredients, sets the clients' preferences as two sets of indexes to access ingrList.
        :param ingrList: a list of strings
        :return: void
        """
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

    return list(set(ingrList))


def update_indexes(clients, ingrList):
    """
    Updates l_ingr and d_ingr of each client given a complete list of ingredients.
    :param clients: the list containing all the clients
    :param ingrList: a list of strings
    :return: void
    """
    for client in clients:
        client.set_indexes(ingrList)


"""
====== FILE PROCESSING ======
"""


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
    otr = str(NIng)
    for idx, spin in enumerate(pizzaChain):  # idx position in chain, spin True or False
        if spin: otr = otr + ' ' + ingrList[idx]
    return otr + "\n"


def outstring_to_pizza_chain(itr, NIng, ingrList):
    """
    To score the final solution, re-parses the output file content to the original binary array.
    (WARNING: NOT TESTED)
    :param itr: the output file content in one line
    :param NIng: the number of ingredients
    :param ingrList: a list of strings with all the ingredients.
    :return: a binary array (0s and 1s) indicating the presence or absence of an ingredient in the solution
    """
    stringPizzaChain = itr.split(" ")[1:]
    pizzaChainIndex = [ingrList.index(item) for item in stringPizzaChain]
    pizzaChain = np.zeros(NIng)
    pizzaChain[pizzaChainIndex] = 1
    return pizzaChain


def read_file(filenameIn):
    """
    Opens the input file and creates the list of clients.
    (WARNING: not used in the final version of the code, only for the example in this script).
    :param filenameIn: the path to the data file
    :return: a tuple containing the number of clients and a preliminary list of clients only with l_ingr_s and d_ingr_s
    """
    with open(filenameIn, 'r') as f:
        data = f.readlines()
    f.close()

    C = int(data[0])
    clients = []
    for cL, cD in zip(data[1::2], data[2::2]):
        cL = cL.split(' ')  # split in an array of words
        cL[-1] = cL[-1].strip('\n')  # remove '\n' from last word
        cD = cD.split(' ')
        cD[-1] = cD[-1].strip('\n')
        clients.append(Client(cL, cD))

    return C, clients


def print_file(filenameOut, ingrList, pizzaChain):
    """
    Converts the binary solution to the output string and prints it to a file.
    (WARNING: not used in the final version of the code, only for the example in this script).
    :param filenameOut: the name of the output file.
    :param ingrList: a list of strings with all the ingredients.
    :param pizzaChain: a binary array (0s and 1s) indicating the presence or absence of an ingredient in the solution
    :return: void
    """
    N = sum(pizzaChain)
    with open(filenameOut, 'w') as f:
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
====== EXAMPLE ======
This example is not executable anymore...
"""

# # These are the parameters you can play with
# fId = 3
# NRepeats = 50
# N1 = 4  # total of survivals
# N2 = 2  # number of descendants per survival
# N0 = N1*N2+N1  # total population
# initialMutRatio = 0.2
# decay = 200
#
# # Here starts the example
# filenames = ["../in/a_an_example.in", \
#              "../in/b_basic.in", \
#              "../in/c_coarse.in", \
#              "../in/d_difficult.in", \
#              "../in/e_elaborate.in"] # Max score for d = 1794 clients in 5h34min (upper limit = 1900 clients)
#
# time_init = time()
# C, clients = read_file(filenames[fId])
# ingrList = gen_ingr(clients)
# NIng = len(ingrList)
# update_indexes(clients, ingrList)
#
# # Initial population
# population = gen_pop_init(N1, NIng)
# scoresN1 = []
# for pizzaChain in population:
#     s = calc_score(clients, pizzaChain)
#     scoresN1.append(s)
# scoresN1 = np.array(scoresN1)  # To be able to use arg sort
# idSorted = np.argsort(-scoresN1)  # sort idx in ascending ording
# populationSorted = population[idSorted]
# scoresN1 = scoresN1[idSorted].tolist()
#
# counter = 0
# generation = 0
# while True:
#     print("---Generetion:" + str(generation))
#     mu = ceil(NIng*initialMutRatio*exp(-generation/decay))
#     populationAugmented = mutate(population, scoresN1, mu)
#     population, scores = filter_by_score(N1, scoresN1, populationAugmented, clients)
#
#     print("Max score:" + str(scores[0]))
#     if scoresN1[0] == scores[0]:
#         counter += 1
#     else:
#         counter = 0
#
#     if counter == NRepeats:
#         break
#
#     scoresN1 = scores
#     generation += 1
#     print("Execution time:" + str(time() - time_init))
#
# print("Final score:" + str(scores[0] / C))
# print_file(filenames[fId][:-2] + "out", ingrList, population[0])
