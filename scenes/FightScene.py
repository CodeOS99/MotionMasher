import numpy as np

import utils.sceneValues
from globals import hand_utils, width, height, mpDraw
import cv2 as cv
import math

class FightScene:
    def __init__(self):
        self.prev_lmks = []

    def draw(self, img):
        imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        hand_utils.open_or_closed(imgRGB, img)

    def update(self, img) -> int:
        return utils.sceneValues.fight_scene
    def shouldQuit(self) -> bool:
         return False
