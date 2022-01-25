class Client:
    def __init__(self, likes, dislikes):
        """likes and dislikes are lists of strings read from file"""
        self.id = 0
        self.L = int(likes[0])  # number of ingredients client likes
        self.D = int(dislikes[0])  # number of ingredients client dislikes
        self.l_ingr_s = likes[1:] # likes as a list of strings
        self.d_ingr_s = dislikes[1:] # dislikes as a list of strings
        self.l_ingr = [] # likes as a list of indexes
        self.d_ingr = [] # dislikes as a list of indexes

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
        self.l_ingr = [ingrList.index(item) for item in self.l_ingr_s]
        self.d_ingr = [ingrList.index(item) for item in self.d_ingr_s]

    def is_coming(self, pizzaChain):
        """
        Returns True if client gives points, False otherwise.
        :param pizzaChain: a binary array (0s and 1s) indicating the presence or absence of an ingredient in the solution
        :return: a boolean
        """
        likesPresence = pizzaChain[self.l_ingr]
        dislikesPresence = pizzaChain[self.d_ingr]
        if 0 in likesPresence or 1 in dislikesPresence:
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
