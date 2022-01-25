import argparse
import igraph as ig
import data_conversion

if __name__ == '__main__':

    flags = data_conversion.read_flags()

    inp = data_conversion.get_in_file_content(data_conversion.inputFiles[flags.fId])
    ns = data_conversion.parse(inp)

    ### GRAPH DEFINITION
    g = data_conversion.create_graph(ns.clients)
    print("Generated graph: ")
    ig.summary(g)
    data_conversion.save_graph(flags.fId, g)
    gg = data_conversion.read_graph(flags.fId)
    print("Stored graph: ")
    ig.summary(gg)


    print("Graph " + flags.fId + " generated successfully")
