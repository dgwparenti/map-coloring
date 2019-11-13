#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import logging
from ortools.constraint_solver import pywrapcp

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
    # initialise model to add variables and constraints
    logger.debug("Instantiating solver")
    solver = pywrapcp.Solver("color_map")
    solver.TimeLimit(3*1000)  # 15 minutes

    # set decision variable: what color each node should have
    logger.debug("Creating variables")
    c = [solver.IntVar(0, node_count - 1, f"c[{i}]") for i in nodes]

    # set constraints - adjacent variables can't be same color
    logger.debug("Creating adjacent constraint")
    for e in edges:
        solver.Add(c[e[0]] != c[e[1]])

    # # # set constraint - symmetry breaking
    # logger.debug("Creating breaking symmetry constraint")
    # for i in range(node_count):
    #     solver.Add(c[i] <= i + 1)

    # set objective - minimize the maximum color number in c
    logger.debug("Setting objective function")
    max_color = solver.Max(c).Var()
    objective = solver.Minimize(max_color, 1)

    # solve model and print status
    db = solver.Phase(c, solver.CHOOSE_MIN_SIZE_LOWEST_MAX, solver.ASSIGN_MIN_VALUE,)

    # print solution if feasible solution found
    solver.NewSearch(db, [objective])
    num_solutions = 0

    logger.debug("Starting search")
    while solver.NextSolution():
        logger.debug("Next solution found")
        # overwrite solution
        num_solutions += 1
        logger.debug(f"Solution found: {num_solutions}")
        logger.debug("Writing solution list")
        c_solution = [int(c[i].Value()) for i in nodes]
        logger.debug("Solution written")
        if (node_count >= 70) and (node_count < 250):
            if num_solutions == 3:
                logger.debug("Finishing search 70 < x < 250")
                solver.FinishCurrentSearch()
        elif (node_count >= 250) and (node_count < 500):
            if num_solutions == 2:
                logger.debug("Finishing search 250 =< x < 500")
                solver.FinishCurrentSearch()
        elif node_count >= 500:
            if num_solutions == 2:
                logger.debug("Finishing search 500 =< x")
                solver.FinishCurrentSearch()
        else:
            continue

    logger.debug("Ending search")
    solver.EndSearch()
    logger.debug("Completed search")
    # logger.debug("Finding n colors used")
    # n_colors_used = max_color.Value() + 1
    # if solver.WallTime() > 10:
    #     logger.debug("Timeout")
    # if num_solutions >= 4:
    #     solver.FinishCurrentSearch()

    logger.debug("Finding n colors used")
    n_colors_used = len(set(c_solution))

    output_data = f"{n_colors_used} 0\n"
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
