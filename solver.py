#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import logging
from ortools.linear_solver import pywraplp

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

file_location = "./data/gc_4_1"
with open(file_location, "r") as input_data_file:
    input_data = input_data_file.read()


def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    first_line = lines[0].split()
    node_count = int(first_line[0])
    edge_count = int(first_line[1])

    logger.debug("Creating edge list")
    edges = []
    for i in range(1, edge_count + 1):
        line = lines[i]
        parts = line.split()
        edges.append((int(parts[0]), int(parts[1])))

    # create range of nodes
    nodes = range(node_count)
    logger.debug(f"Nodes: {node_count}, Edges: {edge_count}")

    # instantiate the solver
    logger.debug("Instantiating solver")
    solver = pywraplp.Solver('graph_coloring',
                             pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)
    logger.debug("Completed instantiating solver")
    # [START Variables]
    # there are two variables color[x,c] = 1 meaning country x has color c, and use[c] which
    # is 1 if the color c has been used

    # build color[x,c]
    color = {}
    logger.debug("Starting to create color[x,c] variables")
    for x in nodes:
        for c in nodes:  # because there can be as many colors as nodes in the worst case
            color[x, c] = solver.IntVar(0, 1, f"color[{x},{c}]")
    logger.debug("Completed to create color[x,c] variables")

    # build use[c]
    logger.debug("Starting to create use[c] variables")
    use = [solver.IntVar(0, 1, f"use[{c}]") for c in nodes]
    logger.debug("Completed to create use[c] variables")
    logger.debug(f"Number of variables: {solver.NumVariables()}")
    # [END Variables]

    # [START constraints]
    # Adjacent countries cannot be the same color
    logger.debug("Starting to build adjacency constraint")
    for e in enumerate(edges):
        for c in nodes:
            solver.Add(color[edges[e[0]][0], c] + color[edges[e[0]][1], c] <=
                       use[c], f"x:{edges[e[0]][0]} + x:{edges[e[0]][1]} <= c:{use[c]}")
    logger.debug("Completed to build adjacency constraint")

    # Each country can only have 1 color
    logger.debug("Starting to build country can only have 1 color constraint")
    for x in nodes:
        solver.Add(solver.Sum([color[x, c] for c in nodes]) == 1)
    logger.debug("Completed to build country can only have 1 color constraint")


    # symmetry breaking
    logger.debug("Starting to build symmetry breaking constraint")
    for x in nodes:
        for c in nodes:
            solver.Add(color[x, c] <= x+1, f"color[{x},{c}]<={x+1}")

    logger.debug(f"Number of constraints: {solver.NumConstraints()}")
    # [END constraints]

    # set objective
    obj = solver.Sum(use)
    objective = solver.Minimize(obj)

    # [START Solve]
    logger.debug("Started solve")
    solver.SetTimeLimit(10*60*1000)
    result = solver.Solve()
    logger.debug("Completed solve")

    # [END solve]

    # [START solution extraction]
    if result == solver.OPTIMAL:
        logger.info("Optimal solution found")
        opt = 1
    elif result == solver.FEASIBLE:
        logger.info("Feasible solution found")
        opt = 0
    elif result == solver.INFEASIBLE:
        logger.info("Problem is infeasible")
    elif result == solver.NOT_SOLVED:
        logger.info("Problem not solved")
    else:
        logger.debug(f"Solver status: {result}")
        logger.debug("Unknown issue")

    if opt in [0, 1]:
        logger.debug("Finding n colors used")
        n_colors_used = int(solver.Objective().Value())
        logger.debug("Found objective value")

        logger.debug("Extracting variable values")
        # loop through color[x,c] and extract elements == 1 only
        c_solution = []
        for x in nodes:
            for c in nodes:
                if color[x, c].SolutionValue() == 1:
                    c_solution.append(c)
        logger.debug("Extracted variable values")

    output_data = f"{n_colors_used} {opt}\n"
    output_data += " ".join(map(str, c_solution))
    logger.debug("Created output_data")
    return output_data


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        logger.debug("Reading file")
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/gc_4_1)')
