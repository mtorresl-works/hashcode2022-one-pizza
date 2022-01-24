import argparse
import igraph as ig
import marina
import numpy as np


if __name__ == '__main__':

    flags = marina.read_flags()

    nNodesAtc = 1703
    ### GRAPH DEFINITION
    g = marina.read_graph(flags.fId)

    anticliqueIdx = marina.read_anticlique(flags.fId, nNodesAtc)
    g.delete_vertices(anticliqueIdx)
    marina.save_graph(flags.fId+'-'+str(len(g.vs)), g)
