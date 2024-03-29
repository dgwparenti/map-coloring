#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import logging

# create development variables
debug_mode = True
file_location = "./data/gc_4_1"

# create logger
logger = logging.getLogger("solver")
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler("solver.log")
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# create formatter and add it to the handlers
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)


def solve_it(input_data):
    # Modify this code to run your optimization algorithm
    if debug_mode:
        with open(file_location, "r") as input_data_file:
            input_data = input_data_file.read()

    # parse the input
    lines = input_data.split("\n")

    first_line = lines[0].split()
    node_count = int(first_line[0])
    edge_count = int(first_line[1])
    logger.debug(f"Nodes: {node_count}, Edges: {edge_count}")

    edges = []
    for i in range(1, edge_count + 1):
        line = lines[i]
        parts = line.split()
        edges.append((int(parts[0]), int(parts[1])))

    # build a trivial solution
    # every node has its own color
    solution = range(0, node_count)

    # prepare the solution in the specified output format
    output_data = str(node_count) + " " + str(0) + "\n"
    output_data += " ".join(map(str, solution))

    return output_data


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        logger.debug(f"File being read: {file_location}")
        with open(file_location, "r") as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print(
            "This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/gc_4_1)"
        )
