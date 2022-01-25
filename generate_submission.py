import argparse
import data_conversion


def read_flags(fId):

        parser = argparse.ArgumentParser()

        parser.add_argument('-fId', help="Input file identifier (str). Default = "+fId, type=str, default=fId)

        return parser.parse_args()


if __name__ == '__main__':

    flags = read_flags(fId='a')

    inp = data_conversion.get_in_file_content(data_conversion.inputFiles[flags.fId])
    ns = data_conversion.parse(inp)
    score, pizzaChain = data_conversion.read_best(flags.fId)
    print("File "+flags.fId)
    print("Submission score: {:d}".format(score))
    data_conversion.print_submission_file(flags.fId, ns.ingrList, score, pizzaChain)
