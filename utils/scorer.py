from time import time


def score_from_graph(antigraph):
    """
    Calculates the score of a subgraph (ideally the maximal anti-clique of some previously treated graph)
    :param antigraph: a graph whose nodes are independent clients
    :return: an int value
    """
    return antigraph.vcount()

def score_from_pizza(clients, pizzaChain):
    """
    Calculates the score of a pizzaChain solution given a list of clients.
    :param clients: the list containing all the clients
    :return: an int value
    """
    #start = time()
    score = 0
    for client in clients:
        if client.is_coming(pizzaChain):
            score = score + 1
    #print("Scorer time = "+str(time()-start))
    return score