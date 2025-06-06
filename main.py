import random

from PIL import ImageGrab
from Controllers import waitForKey, getMousePosition, openSpot, flagSpot, leftClickPosition
from Spot import Spot
from time import sleep
from Solver import makeStep
from LPSolver import calculateProbabilities

EASY = [8, 8, 10]
MID = [16, 16, 40]
HARD = [16, 30, 99]

ROWS, COLS, BOMBS = HARD
TOP_LEFT = None
BOTTOM_RIGHT = None
RESTART = None

MAX_LP_SOLUTIONS = 128

def takeScreenshot():
    # resetMousePosition()
    image = ImageGrab.grab()
    return image

def setupArea():
    global TOP_LEFT, BOTTOM_RIGHT, RESTART, ROWS, COLS
    while TOP_LEFT is None or BOTTOM_RIGHT is None or RESTART is None:
        waitForKey()
        if TOP_LEFT is None:
            TOP_LEFT = getMousePosition()
            print("Top Left Position Set")
            sleep(1)
        elif BOTTOM_RIGHT is None:
            BOTTOM_RIGHT = getMousePosition()
            print("Bottom Right Position Set")
            sleep(1)
        else:
            RESTART = getMousePosition()
            print("Restart Position Set")
            sleep(1)

    # print(f"TOP_LEFT = {TOP_LEFT}\nBOTTOM_RIGHT = {BOTTOM_RIGHT}\nRESTART = {RESTART}")
    # exit()

    xOffset = (BOTTOM_RIGHT[0] - TOP_LEFT[0]) / (COLS - 1)
    yOffset = (BOTTOM_RIGHT[1] - TOP_LEFT[1]) / (ROWS - 1)

    return xOffset, yOffset

def generateBoard(xOffset, yOffset):
    global TOP_LEFT, BOTTOM_RIGHT

    board = []
    for row in range(ROWS):
        board.append([])
        for col in range(COLS):
            position = (TOP_LEFT[0] + col * xOffset, TOP_LEFT[1] + row * yOffset)
            board[row].append(Spot(row, col, position))

    return board

def getValueFromPixel(pixel):
    pixel = (pixel[0], pixel[1], pixel[2])
    if pixel == (255, 255, 255):
        return None
    elif pixel == (255, 255, 0):
        return -1
    elif pixel == (192, 192, 192):
        return 0
    elif pixel == (0, 0, 255):
        return 1
    elif pixel == (0, 128, 0):
        return 2
    elif pixel == (255, 0, 0):
        return 3
    elif pixel == (0, 0, 128):
        return 4
    elif pixel == (128, 0, 0):
        return 5
    elif pixel == (0, 128, 128):
        return 6
    elif pixel == (0, 0, 0):
        return 7
    elif pixel == (255, 255, 255):
        return 8
    exit("Error: INVALID COLOR!")

def scanBoard(board):
    image = takeScreenshot()
    for row in board:
        for spot in row:
            if spot.value is not None:
                continue
            pixel = image.getpixel(spot.position)
            value = getValueFromPixel(pixel)
            spot.calculateValue(board, value)

def isGameFinished():
    global RESTART

    image = takeScreenshot()
    pixel = image.getpixel(RESTART)
    pixel = (pixel[0], pixel[1], pixel[2])
    return pixel == (255, 0, 0) or pixel == (0, 128, 0)

def markLPSolverDetections(board, probabilities):
    lowestProb, lowestPos = 1, None
    hasBestCase = False
    for pos, prob in probabilities.items():
        if prob < lowestProb:
            lowestProb = prob
            lowestPos = pos
        if prob not in [0, 1]:
            continue
        hasBestCase = True
        row, col = pos
        tile = board[row][col]
        if prob == 0:
            openSpot(tile)
        else:
            flagSpot(board, tile)
    if not hasBestCase:
        try:
            print(f"No best case found! Opening a spot with {lowestProb} probability of being a bomb")
            row, col = lowestPos
            tile = board[row][col]
            openSpot(tile)
        except:
            openRandomSpot(board)

def restartGame():
    global RESTART
    leftClickPosition(RESTART)

def openRandomSpot(board):
    n, m = len(board), len(board[0])
    row, col = random.randrange(n), random.randrange(m)
    while board[row][col].value is not None:
        row, col = random.randrange(m), random.randrange(m)

    openSpot(board[row][col])

def main():
    xOffset, yOffset = setupArea()

    while True:
        board = generateBoard(xOffset, yOffset)

        while not isGameFinished():
            scanBoard(board)
            isImproved = makeStep(board)
            if not isImproved:
                probabilities = calculateProbabilities(board, MAX_LP_SOLUTIONS)
                markLPSolverDetections(board, probabilities)
        print("Game Finished! Waiting for input")
        waitForKey()
        restartGame()

if __name__ == "__main__":
    main()
