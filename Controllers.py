import time

from pynput.mouse import Controller as MController, Button
from pynput.keyboard import Controller as KController, Key, Listener

MOUSE = MController()
KEYBOARD = KController()

LEFT_CLICK = Button.left
RIGHT_CLICK = Button.right

TARGET_KEY = 'k'

def openSpot(board, spot):
    MOUSE.position = spot.position
    MOUSE.click(LEFT_CLICK)

def flagSpot(board, spot):
    MOUSE.position = spot.position
    # MOUSE.click(RIGHT_CLICK)
    spot.updateNeighborsFlag(board)
    spot.value = -1

def rightClickSpot(spot):
    MOUSE.position = spot.position
    MOUSE.click(RIGHT_CLICK)

def getMousePosition():
    return MOUSE.position

def resetMousePosition():
    MOUSE.position = (0, 0)

def setMousePosition(position):
    MOUSE.position = position

def waitForKey():
    def onPress(key):
        try:
            if key.char == TARGET_KEY:
                return False
        except AttributeError:
            pass

    with Listener(on_press=onPress) as listener:
        listener.join()

    return True
