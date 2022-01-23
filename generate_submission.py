import argparse
import marina


def read_flags(fId):

        parser = argparse.ArgumentParser()

        parser.add_argument('-fId', help="Input file identifier (str). Default = "+fId, type=str, default=fId)

        return parser.parse_args()


if __name__ == '__main__':

    flags = read_flags(fId='a')

    inp = marina.get_in_file_content(marina.inputFiles[flags.fId])
    ns = marina.parse(inp)
    score, pizzaChain = marina.read_best(flags.fId)
    print("File "+flags.fId)
    print("Submission score: {:d}".format(score))
    marina.print_submission_file(flags.fId, ns.ingrList, pizzaChain)
