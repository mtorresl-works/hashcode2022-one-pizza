#### UNDER WORK

##########

# Template for Google Hash Code
to make it easier to deploy an incremental approach. _Automating the booring parts._

## Overview
Input files are stored in `./input_data`

Best configurations are stored in `./best_runs` (score and np.array of 1s and 0s)
Configurations obtained by the greedy graph algorithm are stored in `./greedy_pizzas`

To run a MC solver run `python3 solver-sa.py -fId a -iC best` or `python3 solver-sa.py -fId b -iC best`

To transform best configuration into submission file run `python3 generate_submission.py -fId a` (a, b, c, d or e)
Submission files are in `./output_data`

---- IMPORTANT -----

If you achieve a maximum score in local, generate submission file before pushing to remote repo.

## MC Solvers
MC Solvers (`solver-sa.py` and `solver-aga.py`) look for best configuration indefinitely.
If they hit a configuration scoring higher than configurations in `./best_runs` they overwrite the configuration.
They are stochastic, consider multi-threading.

They can start from a random config, the best config stored in `./best_runs` and the config obtained from the greedy algorithm on the graph. Specified by `-iC` flag
Run `python3 solver-sa.py --help` or `python3 solver-sa.py --help` for details on the solver flags.

---- IMPORTANT -----
`solver-aga.py` performs better than `solver-sa.py`

## Graph solver
Solves maximal independent set for a given graph using a greedy algorithm (deterministic)


## Other:

-`marina.py`: object definition and function tool box (calculate score, read and print files, graphs, etc.)

-`package.sh`: TO BE WRITTEN (zips scripts for submission)




## Nice to have for the competition:
- `pypy3` faster execution, because of JiT compilation to C
    + MacOS: `brew install pypy3`
    + Ubuntu: `sudo apt-get install pypy3`
    + Arch: `sudo pacman -S pypy3`
