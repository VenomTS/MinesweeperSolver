from Controllers import flagSpot, openSpot, rightClickSpot
from copy import deepcopy

def makeStep(board):
    rows, cols = len(board), len(board[0])
    isImproved = openAllNeighbors(board, rows, cols)
    isImproved = isImproved or flagAllNeighbors(board, rows, cols)
    return isImproved

# Number of bombs == 0
def openAllNeighbors(board, rows, cols):
    isImproved = False

    rowOffsets = [-1, -1, -1, 0, 0, 1, 1, 1]
    colOffsets = [-1, 0, 1, -1, 1, -1, 0, 1]

    for row in board:
        for spot in row:
            if spot.value != 0 or spot.countClosedNeighbors(board) == 0:
                continue

            row = spot.row
            col = spot.col
            for rowOffset, colOffset in zip(rowOffsets, colOffsets):
                newRow = row + rowOffset
                newCol = col + colOffset
                if newRow < 0 or newCol < 0 or newRow >= rows or newCol >= cols:
                    continue

                neighbor = board[newRow][newCol]
                if neighbor.value is None:
                    openSpot(board, neighbor)
                    isImproved = True
    return isImproved

def flagAllNeighbors(board, rows, cols):
    isImproved = False

    rowOffsets = [-1, -1, -1, 0, 0, 1, 1, 1]
    colOffsets = [-1, 0, 1, -1, 1, -1, 0, 1]

    for row in board:
        for spot in row:
            if spot.value is None or spot.value <= 0 or spot.countClosedNeighbors(board) != spot.value:
                continue

            row = spot.row
            col = spot.col
            for rowOffset, colOffset in zip(rowOffsets, colOffsets):
                newRow = row + rowOffset
                newCol = col + colOffset
                if newRow < 0 or newCol < 0 or newRow >= rows or newCol >= cols:
                    continue

                neighbor = board[newRow][newCol]
                if neighbor.value is None:
                    flagSpot(board, neighbor)
                    isImproved = True
    return isImproved

def calculateFoundBombCount(board):
    count = 0
    for row in board:
        for item in row:
            if item.value is None:
                continue
            if item.value == -1:
                count += 1
    return count

def isBoardSatisfied(board):
    for row in board:
        for item in row:
            if item.value is None:
                continue
            # If we find a spot that still has bombs, well, we must search still
            if item.value >= 1:
                return False
    return True

def recursiveMineFinder(board, edges, placeableMines):
    if isBoardSatisfied(board):
        return True

    if placeableMines == 0:
        return False

    for i in range(len(edges)):
        currEdge = edges[i]
        if not currEdge.canSpotBeBomb(board):
            continue
        currEdge.updateNeighborsFlag(board)
        if recursiveMineFinder(board, edges[i + 1:], placeableMines - 1):
            currEdge.recursiveMineCount += 1
        currEdge.updateNeighborsUnflag(board)

    return False


def calculateOddsPerSpot(board, minesTotal):
    edges = []
    for row in board:
        for item in row:
            item.recursiveMineCount = 0
            if item.isEdge(board):
                edges.append(item)
                rightClickSpot(item)

    placeableMines = minesTotal - calculateFoundBombCount(board)

    recursiveMineFinder(board, edges, placeableMines)
    for row in board:
        for item in row:
            print(item.recursiveMineCount, end=' ')
        print()
    exit()
