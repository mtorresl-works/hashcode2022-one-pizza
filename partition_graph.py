import argparse
import igraph as ig
import utils.data_conversion as data_conversion
import utils.read_write as read_write
import numpy as np
import matplotlib.pyplot as plt
import random

def flatten(t):
    return [item for sublist in t for item in sublist]

if __name__ == '__main__':

    flags = data_conversion.read_flags()
    fId = flags.fId

    ### GRAPH DEFINITION
    gRaw = read_write.read_graph(fId, anticlique=False, NVertex = 4986)
    gAnti = read_write.read_graph(fId, anticlique=True, NVertex = 2072)

    #client ids correspond to vertices ids in parent graph only
    allIds = [c.id for c in gRaw.vs['client_info']]
    idsAnti = [c.id for c in gAnti.vs['client_info']]
    i=0
    gChild = gRaw.copy()
    gAntiStored = gRaw.copy()

    #gRaw.vs[idsAnti][:100].neighbors.delete()
    nAnticlique=len(gAnti.vs)
    nKills = 100
    killIds = random.sample(idsAnti, nKills)
    liveIds = set(idsAnti)-set(killIds)



    neigh = flatten(gChild.neighborhood(vertices=gChild.vs[killIds], order=1, mode='all'))
    gChild.delete_vertices(neigh)
    gAntiStored.delete_vertices(set(allIds)-liveIds)
    #gAnti.delete_vertices(gAnti.vs['client_info'][killIds])
    print(len(gChild.vs))
    print(len(gAntiStored.vs))

    # for v in gRaw.vs[idsAnti]:
    #     neigh = gRaw.neighbors(v, mode='all')
    #     idsNeigh = [c.id  for c in gRaw.vs[neigh]['client_info']]
    #     idsCopy = [c.id for c in gCopy.vs['client_info']]
    #
    #     seq = [id for id in idsNeigh if id in idsCopy]
    #     gCopy.delete_vertices(seq)

    # print(len(gAnti1))
    # idsAnti2 = [c.id for c in gAnti2.vs['client_info']]
    #
    # idsDiff = list( set(idsAnti2) - set(idsAnti1))
    #
    # print(len(gAnti1.vs))
    #
    # for id in idsDiff:
    #     gCopy = gRaw.copy()
    #     antiComplementary = list(set(allIds) - set(idsAnti1) - set([id]))
    #
    #     gCopy.delete_vertices(gCopy.vs[antiComplementary])
    #
    #     if len(gCopy.vs.select(_degree=0))>len(idsAnti1):
    #         idsAnti1.append(id)
    #         print("+1")


    # print(len(gCopy.vs))
    # # gRaw.delete_vertices(gRaw.vs[idsNotInAntis])
    # print(len(gRaw.vs[idsNotInAntis].select(_degree_le=2)))
    # print(len(idsNotInAntis))
    # quots = []
    # ls = []
    # deg = []
    # for i in range(max(gRaw.vs.degree())):
    #     d = len(gRaw.vs.select(_degree=i))
    #     if not d==0:
    #         l = len(gRaw.vs[idsAnti].select(_degree=i))
    #         quots.append(l/d)
    #         deg.append(i)
    #         ls.append(l)

    # seq = gRaw.vs.select(_degree_ge=17) #greater than
    # print(len(seq))
    # gRaw.delete_vertices(seq)
    # read_write.export_graph(fId, gRaw, anticlique=False)
    #

    # data = np.array(gRaw.vs[idsAnti1].degree())
    # d = np.diff(np.unique(data)).min()
    # left_of_first_bin = data.min() - float(d)/2
    # right_of_last_bin = data.max() + float(d)/2
    # plt.hist(data, np.arange(left_of_first_bin, right_of_last_bin + d, d))

    # plt.plot(deg, ls, 'o-')
    # plt.show()
