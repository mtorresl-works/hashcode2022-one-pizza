import argparse
import igraph as ig
import data_conversion
import numpy as np


if __name__ == '__main__':

    flags = data_conversion.read_flags()

    nNodesAtc = 1703
    ### GRAPH DEFINITION
    g = data_conversion.read_graph(flags.fId)

    anticliqueIdx = data_conversion.read_anticlique(flags.fId, nNodesAtc)
    g.delete_vertices(anticliqueIdx)
    data_conversion.save_graph(flags.fId + '-' + str(len(g.vs)), g)
