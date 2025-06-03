class Spot:
    def __init__(self, row, col, position):
        # None = Closed
        # -1 = Bomb
        # 0-8 - Number of Bombs around
        self.value = None
        self.row = row
        self.col = col
        self.position = position

    def calculateValue(self, board, value):
        if value is None:
            return

        self.value = value

        rowOffsets = [-1, -1, -1, 0, 0, 1, 1, 1]
        colOffsets = [-1, 0, 1, -1, 1, -1, 0, 1]

        rows = len(board)
        cols = len(board[0])

        for rowOffset, colOffset in zip(rowOffsets, colOffsets):
            newRow = self.row + rowOffset
            newCol = self.col + colOffset

            if newRow < 0 or newCol < 0 or newRow >= rows or newCol >= cols:
                continue

            neighbor = board[newRow][newCol]
            if neighbor.value == -1:
                self.value -= 1


    def updateNeighborsFlag(self, board):
        rowOffsets = [-1, -1, -1, 0, 0, 1, 1, 1]
        colOffsets = [-1, 0, 1, -1, 1, -1, 0, 1]

        rows = len(board)
        cols = len(board[0])

        for rowOffset, colOffset in zip(rowOffsets, colOffsets):
            newRow = self.row + rowOffset
            newCol = self.col + colOffset

            if newRow < 0 or newCol < 0 or newRow >= rows or newCol >= cols:
                continue

            neighbor = board[newRow][newCol]
            if neighbor.value in [None, -1]:
                continue
            if neighbor.value == 0:
                print("GRESKA - OZNACAVA SE SPOT KOJI NE MOZE IMATI VISE MINA OKO SEBE")
            else:
                neighbor.value -= 1

    def countClosedNeighbors(self, board):
        rowOffsets = [-1, -1, -1, 0, 0, 1, 1, 1]
        colOffsets = [-1, 0, 1, -1, 1, -1, 0, 1]

        count = 0

        rows = len(board)
        cols = len(board[0])

        for rowOffset, colOffset in zip(rowOffsets, colOffsets):
            newRow = self.row + rowOffset
            newCol = self.col + colOffset

            if newRow < 0 or newCol < 0 or newRow >= rows or newCol >= cols:
                continue

            neighbor = board[newRow][newCol]
            if neighbor.value is None:
                count += 1
        return count