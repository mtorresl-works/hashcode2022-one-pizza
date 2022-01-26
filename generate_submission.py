import argparse
import utils.read_write as read_write
import utils.data_conversion as data_conversion



if __name__ == '__main__':

    flags = data_conversion.read_flags()

    fId = flags.fId
    ns = data_conversion.create_client_ns(fId)

    graph = read_write.read_graph(fId, folder)

    score, pizzaChain = data_conversion.read_best(flags.fId)
    print("File "+flags.fId)
    print("Submission score: {:d}".format(score))
    data_conversion.print_submission_file(flags.fId, ns.ingrList, score, pizzaChain)
