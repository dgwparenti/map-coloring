#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import logging
from ortools.constraint_solver import pywrapcp

# create development variables
debug_mode = False
file_location = "./data/gc_4_1"

# create logger
logger = logging.getLogger("solver")
logger.setLevel(logging.INFO)
# create file handler which logs even debug messages
fh = logging.FileHandler("solver.log")
fh.setLevel(logging.INFO)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
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

    # create range of nodes
    nodes = range(node_count)
    logger.debug(f"List of nodes: {nodes}")

    # initialise model to add variables and constraints
    solver = pywrapcp.Solver("color_map")

    # set decision variable: what color each node should have
    c = [solver.IntVar(0, node_count - 1, f"c[{i}]") for i in nodes]

    # set constraints - adjacent variables can't be same color
    logger.debug("Setting constraint - adjacent nodes different")
    for e in edges:
        logger.debug(f"{c[e[0]]} != {c[e[1]]}")
        solver.Add(c[e[0]] != c[e[1]])

    # # set constraint - symmetry breaking
    logger.debug("Setting constraint - symmetry breaking")
    for i in range(node_count):
        logger.debug(f"c[{i}] <= {i+1}")
        solver.Add(c[i] <= i + 1)

    # set objective - minimize the maximum color number in c
    max_color = solver.Max(c).Var()
    objective = solver.Minimize(max_color, 1)

    # solve model and print status
    db = solver.Phase(c, solver.CHOOSE_MIN_SIZE_LOWEST_MAX, solver.ASSIGN_MIN_VALUE,)

    # print solution if feasible solution found
    solver.NewSearch(db, [objective])
    num_solutions = 0

    while solver.NextSolution():
        # overwrite solution
        num_solutions += 1
        c_solution = [int(c[i].Value()) for i in nodes]
        n_colors_used = max_color.Value() + 1

    solver.EndSearch()
    logger.info(f"Solution: {c_solution}")
    logger.info(f"Colors used: {n_colors_used}")

    # prepare the solution in the specified output format
    # output_data = str(node_count) + " " + str(0) + "\n"
    # output_data += " ".join(map(str, solution))

    output_data = f"{n_colors_used} 0\n"
    output_data += " ".join(map(str, c_solution))

    return output_data


if __name__ == "__main__":

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
