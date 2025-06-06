class Spot:
    def __init__(self, row, col, position):
        # None = Closed
        # -1 = Bomb
        # 0-8 - Number of Bombs around
        self.value = None
        self.row = row
        self.col = col
        self.position = position
        self.recursiveMineCount = 0

    def getNeighbors(self, board):
        neighbors = []

        rowOffsets = [-1, -1, -1, 0, 0, 1, 1, 1]
        colOffsets = [-1, 0, 1, -1, 1, -1, 0, 1]

        rows = len(board)
        cols = len(board[0])

        for rowOffset, colOffset in zip(rowOffsets, colOffsets):
            newRow = self.row + rowOffset
            newCol = self.col + colOffset

            if newRow < 0 or newCol < 0 or newRow >= rows or newCol >= cols:
                continue

            neighbors.append(board[newRow][newCol])
        return neighbors

    def calculateValue(self, board, value):
        if value is None:
            return
        self.value = value

        for neighbor in self.getNeighbors(board):
            if neighbor.value == -1:
                self.value -= 1

    # Used for flagging the spot as bomb and updating all the neighbors
    def updateNeighborsFlag(self, board):
        for neighbor in self.getNeighbors(board):
            if neighbor.value in [None, -1]:
                continue

            if neighbor.value == 0:
                print("GRESKA - OZNACAVA SE SPOT KOJI NE MOZE IMATI VISE MINA OKO SEBE")

            else:
                neighbor.value -= 1

    def updateNeighborsUnflag(self, board):
        for neighbor in self.getNeighbors(board):
            if neighbor.value in [None, -1]:
                continue

            # I unflagged the spot, thus neighbor has +1 bombs around (since this is not one of them)
            neighbor.value += 1

    def canSpotBeBomb(self, board):
        for neighbor in self.getNeighbors(board):
            if neighbor.value in [None, -1]:
                continue
            if neighbor.value == 0:
                return False
        return True

    # Edges are places that have contact with at least one open spot and are closed themselves
    def isEdge(self, board):
        if self.value is not None:
            return False

        for neighbor in self.getNeighbors(board):
            if neighbor.value in [None, -1]:
                continue
            if neighbor.value >= 1:
                return True
        return False

    def countClosedNeighbors(self, board):
        count = 0
        for neighbor in self.getNeighbors(board):
            if neighbor.value is None:
                count += 1
        return count