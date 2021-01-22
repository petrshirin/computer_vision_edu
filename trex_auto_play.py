import pyautogui
from time import sleep
import cv2
import numpy as np
import mss

time_to_wait = 0.1
wall_cell = {'top': 689, 'left': 385, 'width': 760 - 689, 'height': 463 - 385}


def jump():
    pyautogui.keyDown('space')
    sleep(time_to_wait)
    pyautogui.keyUp('space')


def check_wall(screen):
    img = screen.grab(wall_cell)
    img = np.array(img)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    print(img)
    return np.mean(cv2.Canny(img, 200, 300))


if __name__ == '__main__':
    screen = mss.mss()
    while True:
        if check_wall(screen):
            jump()
            sleep(1)
