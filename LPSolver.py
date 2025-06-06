import time

import pulp
from collections import defaultdict
from Controllers import rightClickSpot

def calculateProbabilities(board, maxSolutions):
    rows, cols = len(board), len(board[0])

    problem = pulp.LpProblem("MinesweeperSolver", pulp.LpMinimize)

    variables = {}
    for row in range(rows):
        for col in range(cols):
            tile = board[row][col]
            # None = Closed
            if tile.isEdge(board):
                var = pulp.LpVariable(f"x_{row}_{col}", cat='Binary')
                variables[(row, col)] = var

    for row in range(rows):
        for col in range(cols):
            tile = board[row][col]
            # We do not care about closed tiles, mines or tiles with no mines around
            if tile.value in [None, 0, -1]:
                continue

            unknowns = []
            # We are only interested in closed neighbors
            for neighbor in tile.getNeighbors(board):
                if neighbor.value is not None:
                    continue
                unknowns.append((neighbor.row, neighbor.col))

            # We only interested in tiles that actually have unknowns, aka edge tiles
            if not unknowns:
                continue

            # The number of 1s among neighbors must be equal to the tile's number
            constraint = pulp.lpSum([variables[pos] for pos in unknowns]) == tile.value
            print(constraint)
            problem += constraint

    # Actual Solve
    validSolutions = []

    for _ in range(maxSolutions):
        print(f"Iteration {_} / {maxSolutions}")
        status = problem.solve()
        # No more solutions
        if status != pulp.LpStatusOptimal:
            break

        # for pos, var in variables.items():
        #     print(f"Pos: {pos} | Var: {var} | Var's Value: {pulp.value(var)}")
        #
        # exit()

        currentSolution = {pos: int(pulp.value(var)) for pos, var in variables.items()}
        validSolutions.append(currentSolution)

        exclude = pulp.lpSum([
            (1 - variables[pos]) if val == 1 else variables[pos]
            for pos, val in currentSolution.items()
        ])

        problem += exclude >= 1

    # Calculate probabilities
    mineCounts = defaultdict(int)
    for solution in validSolutions:
        for pos, isMine in solution.items():
            mineCounts[pos] += isMine

    total = len(validSolutions)
    probabilities = {pos: mineCounts[pos] / total for pos in variables}

    return probabilities

    # print(f"Found {total} valid mine configurations.")
    # for pos, prob in probabilities.items():
    #     print(f"Tile {pos} has a {prob:.2%} chance of being a mine")
    #     print(f"0 = {prob == 0} | 100 = {prob == 100} | Real Prob = {prob}")