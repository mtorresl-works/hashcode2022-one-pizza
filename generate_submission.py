import argparse
import utils.read_write as read_write
import utils.data_conversion as data_conversion



if __name__ == '__main__':

    flags = data_conversion.read_flags()

    fId = flags.fId

    ns = data_conversion.create_client_ns(fId)

    if is_graph:
        NVertex = flags.NV
        graph = read_write.read_graph(fId, anticlique=True, NVertex=NVertex)

        pizzaChain = data_conversion.graph_to_pizza(graph, ns.NIng)

        score = score_from_pizza(ns.clients, pizzaChain)

        export_pizza(fId, score, method='or', pizzaChain)

        if not score == NVertex:
            print('Something went wrong...')

    else:
        score, pizzaChain = read_pizza(fId, method='mc')

        
    print("File "+flags.fId)
    print("Submission score: {:d}".format(score))
    oStr = data_conversion.pizzaChain_to_outstring(ppizzaChain, ns.Ning, ns.ingrList)
    read_write.string_to_submission_file(oStr, fId, score)
