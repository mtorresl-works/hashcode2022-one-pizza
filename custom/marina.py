from math import *
import numpy as np
from time import time


class Client:
    def __init__(self, likes, dislikes):
        """likes and dislikes are lists of strings read from file"""
        self.L = int(likes[0])  # number of ingredients client likes
        self.D = int(dislikes[0])  # number of ingredients client dislikes
        self.l_ingr_s = likes[1:]
        self.d_ingr_s = dislikes[1:]
        self.l_ingr = []
        self.d_ingr = []

    #
    def set_indexes(self, ingrList):
        self.l_ingr = {ingrList.index(item) for item in self.l_ingr_s}
        self.d_ingr = {ingrList.index(item) for item in self.d_ingr_s}

    def is_coming(self, pizzaChain):
        """Returns True if client gives points, False otherwise."""
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


# def read_file(filenameIn):
#     with open(filenameIn, 'r') as f:
#         data = f.readlines()
#     f.close()
#
#     C = int(data[0])
#     clients = []
#     for cL, cD in zip(data[1::2], data[2::2]):
#         cL = cL.split(' ')  # split in an array of words
#         cL[-1] = cL[-1].strip('\n')  # remove '\n' from last word
#         cD = cD.split(' ')
#         cD[-1] = cD[-1].strip('\n')
#         clients.append(Client(cL, cD))

def read_file(filestring):
    data = filestring.split('\n')
    C = int(data[0])
    clients = []
    for cL, cD in zip(data[1::2], data[2::2]):
        cL = cL.split(' ')  # split in an array of words
        cD = cD.split(' ')
        clients.append(Client(cL, cD))

    return C, clients


def gen_ingr(clients):
    ingrList = []
    for c in clients:
        ingrList += c.l_ingr_s
        ingrList += c.d_ingr_s

    return list(set(ingrList))

def update_indexes(clients, ingrList):
    for client in clients:
        client.set_indexes(ingrList)

def gen_pop_init(N0, NIng):
    return np.random.randint(2, size=(N0, NIng))


# function for implementing the single-point crossover
def crossover(l, q):
    a, b = l.copy(), q.copy()
    # generating the random number to perform crossover
    k = np.random.randint(NIng)
    # interchanging the genes
    a[k:], b[k:] = q[k:].copy(), l[k:].copy()
    return a,b

def mutate(popSurvivals, scores, mu):
    weights = scores/np.sum(scores)
    #Choosing the parents
    random_parents = np.random.choice(range(N1), N1*N2, p=weights)

    #Crossover
    children = np.zeros((N1*N2, NIng))
    for i in range(N1*N2-1):
        children[i], children[i+1] = crossover(popSurvivals[random_parents[i]], popSurvivals[random_parents[i+1]])
    # children =np.tile(popSurvivals, (N2,1))

    #Mutate the children
    mutations = np.zeros((N1*N2, NIng))
    ones = np.ones((N1*N2, mu))
    random_ingr = np.random.choice(NIng, (N1*N2, mu))
    list(map(lambda mut, i: np.put(mut, random_ingr[i], ones), mutations, range(N1*N2)))
    return np.concatenate((popSurvivals, np.logical_xor(children,mutations)), axis=0)


def print_file(filenameOut, ingrSet, pizzaChain):
    N = sum(pizzaChain)
    with open(filenameOut, 'w') as f:
        f.write(str(N))
        for idx, spin in enumerate(pizzaChain):  # idx position in chain, spin True or False
            if spin: f.write(' ' + ingrSet[idx])
        f.write('\n')
    f.close()

def outstring_to_pizza_chain(itr, NIng, ingrList):
    stringPizzaChain = itr.split(" ")[1:]
    pizzaChainIndex = [ingrList.index(item) for item in stringPizzaChain]
    pizzaChain = np.zeros(NIng)
    pizzaChain[pizzaChainIndex] = 1
    return pizzaChain


def calc_score(clients, pizzaChain):
    score = 0
    for client in clients:
        if client.is_coming(pizzaChain):
            score = score + 1
    return score


def filter_by_score(n1, scoresN1, population, clients):
    """population is an np.array (dtype=object) of pizzaChains of size N1 + N1*N2.
    N1 is the size of the surviving population.
    The first N1 elements in population are the parents whose score is known (scoresN1)"""
    scores = scoresN1
    for pizzaChain in population[n1:]:
        s = calc_score(clients, pizzaChain)
        scores.append(s)

    scores = np.array(scores)  # To be able to use arg sort
    idSorted = np.argsort(-scores)  # sort idx in ascending ording
    populationSorted = population[idSorted]
    scoresSorted = scores[idSorted]

    return populationSorted[:n1], list(scoresSorted[:n1])


filenames = ["./a_an_example.in.txt", \
             "./b_basic.in.txt", \
             "./c_coarse.in.txt", \
             "./d_difficult.in.txt", \
             "./e_elaborate.in.txt"] # Max score for d = 1794 clients in 5h34min (upper limit = 1900 clients)
filenames = ["./input_data/a_an_example.in.txt", \
             "./input_data/b_basic.in.txt", \
             "./input_data/c_coarse.in.txt", \
             "./input_data/d_difficult.in.txt", \
             "./input_data/e_elaborate.in.txt"]

fId = 3
NRepeats = 50
N1 = 40  # total of survivals
N2 = 2  # number of descendants per survival
N0 = N1*N2+N1  # total population
initialMutRatio = 0.2
decay = 200


time_init = time()
C, clients = read_file(filenames[fId])
ingrList = gen_ingr(clients)
NIng = len(ingrList)
update_indexes(clients, ingrList)

# Initial population
population = gen_pop_init(N1, NIng)
scoresN1 = []
for pizzaChain in population:
    s = calc_score(clients, pizzaChain)
    scoresN1.append(s)
scoresN1 = np.array(scoresN1)  # To be able to use arg sort
idSorted = np.argsort(-scoresN1)  # sort idx in ascending ording
populationSorted = population[idSorted]
scoresN1 = scoresN1[idSorted].tolist()

counter = 0
generation = 0
while True:
    print("---Generetion:" + str(generation))
    mu = ceil(NIng*initialMutRatio*exp(-generation/decay))
    populationAugmented = mutate(population, scoresN1, mu)
    population, scores = filter_by_score(N1, scoresN1, populationAugmented, clients)

    print("Max score:" + str(scores[0]))
    if scoresN1[0] == scores[0]:
        counter += 1
    else:
        counter = 0

    if counter == NRepeats:
        break

    scoresN1 = scores
    generation += 1
    print("Execution time:" + str(time() - time_init))

print("Final score:" + str(scores[0] / C))
print_file(filenames[fId][:-6] + "out", ingrList, population[0])

#esto es una prueba
#y esto es otra prueba
