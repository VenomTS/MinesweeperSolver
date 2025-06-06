from PIL import ImageGrab
from Controllers import waitForKey, getMousePosition
from Spot import Spot
from time import sleep
from Solver import makeStep, calculateOddsPerSpot

EASY = [8, 8, 10]
MID = [16, 16, 40]
HARD = [16, 30, 99]

ROWS, COLS, BOMBS = HARD
TOP_LEFT = None
BOTTOM_RIGHT = None
RESTART = None

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
    # Have to add 255 as last parameter
    # None = (255, 255, 255) (Closed)
    # Flagged = (255, 255, 0)
    # 0 = (192, 192, 192)
    # 1 = (0, 0, 255)
    # 2 = (0, 128, 0)
    # 3 = (255, 0, 0)
    # 4 = (0, 0, 128)
    # 5 = (128, 0, 0)
    # 6 = (0, 128, 128)
    # 7 = (0, 0, 0)
    # 8 = (128, 128, 128)
    #
    # DEAD = (255, 0, 0)
    # ALIVE = (255, 255, 0)
    # WON = (0, 128, 0)
    if pixel == (255, 255, 255, 255):
        return None
    elif pixel == (255, 255, 0, 255):
        return -1
    elif pixel == (192, 192, 192, 255):
        return 0
    elif pixel == (0, 0, 255, 255):
        return 1
    elif pixel == (0, 128, 0, 255):
        return 2
    elif pixel == (255, 0, 0, 255):
        return 3
    elif pixel == (0, 0, 128, 255):
        return 4
    elif pixel == (128, 0, 0, 255):
        return 5
    elif pixel == (0, 128, 128, 255):
        return 6
    elif pixel == (0, 0, 0, 255):
        return 7
    elif pixel == (255, 255, 255, 255):
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
    return pixel == (255, 0, 0, 255) or pixel == (0, 128, 0, 255)

def main():
    xOffset, yOffset = setupArea()
    board = generateBoard(xOffset, yOffset)

    while not isGameFinished():
        scanBoard(board)
        isImproved = makeStep(board)
        if not isImproved:
            print("Started Doing Recursion")
            calculateOddsPerSpot(board, BOMBS)

def printBoard(board):
    for row in board:
        for item in row:
            value = item.value
            if value is None:
                print("X", end=" ")
            elif value == -1:
                print("B", end=" ")
            else:
                print(value, end=" ")
        print()
    exit()

if __name__ == "__main__":
    main()
