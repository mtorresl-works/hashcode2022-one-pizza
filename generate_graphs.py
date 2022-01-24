import argparse
import igraph as ig
import marina

if __name__ == '__main__':

    flags = marina.read_flags()

    inp = marina.get_in_file_content(marina.inputFiles[flags.fId])
    ns = marina.parse(inp)

    ### GRAPH DEFINITION
    g = marina.create_graph(ns.clients)
    print("Generated graph: ")
    ig.summary(g)
    marina.save_graph(flags.fId, g)
    gg = marina.read_graph(flags.fId)
    print("Stored graph: ")
    ig.summary(gg)


    print("Graph " + flags.fId + " generated successfully")
