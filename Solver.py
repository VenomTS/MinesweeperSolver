from Controllers import flagSpot, openSpot

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

