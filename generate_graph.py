import igraph as ig
import utils.read_write as read_write
import utils.data_conversion as data_conversion

if __name__ == '__main__':

    folder = 'data_graphs_raw'
    flags = data_conversion.read_flags()

    fId = flags.fId
    ns = data_conversion.create_client_ns(fId)

    ### GRAPH DEFINITION
    g = data_conversion.clients_to_graph(ns.clients)
    print("Generated graph: ")
    ig.summary(g)
    read_write.export_graph(fId, g, folder)
    gg = read_write.read_graph(fId, folder)
    print("Stored graph: ")
    ig.summary(gg)


    print("Graph " + fId + " generated successfully")
