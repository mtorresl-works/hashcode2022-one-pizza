import argparse
import igraph as ig
import utils.data_conversion as data_conversion
import utils.read_write as read_write
import numpy as np
import matplotlib.pyplot as plt


if __name__ == '__main__':

    flags = data_conversion.read_flags()
    fId = flags.fId

    ### GRAPH DEFINITION
    gRaw = read_write.read_graph(fId, anticlique=False, NVertex = 4986)
    gAnti = read_write.read_graph(fId, anticlique=True, NVertex = 2059)

    idsAnti = [c.id for c in gAnti.vs['client_info']]

    quots = []
    ls = []
    deg = []
    for i in range(max(gRaw.vs.degree())):
        d = len(gRaw.vs.select(_degree=i))
        if not d==0:
            l = len(gRaw.vs[idsAnti].select(_degree=i))
            quots.append(l/d)
            deg.append(i)
            ls.append(l)

    plt.plot(deg, ls, 'o-')
    plt.show()
