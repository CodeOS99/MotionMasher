import cv2 as cv

import utils.sceneValues
from utils.UI.button import Button
from utils.colours import *
from globals import hand_utils, width, height

class FightOrTrainMenuScene:
    # FOTM_Scene
    def __init__(self):
        self.fight_option_btn = Button(1/4 * width, height/2 - 90, 200, 100, orange, "FIGHT!")
        self.back_option_btn = Button(0, 0, 200, 100, purple, "Back")
        self.train_option_btn = Button(3/4 * width, height/2 - 90, 200, 100, green, "TRAIN!")
        self.quit_btn = Button(width-200, height-100, 200, 100, red, "QUIT")

        self.BUTTONS = (self.fight_option_btn, self.back_option_btn, self.train_option_btn, self.quit_btn)

    def draw(self, img) -> None:
        for btn in self.BUTTONS:
            btn.draw(img)

    def update(self, img) -> int:
        for btn in self.BUTTONS:
            btn.update(img)

        imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        hand_utils.open_or_closed(imgRGB, img)

        if self.back_option_btn.clicked:
            return utils.sceneValues.main_scene
        if self.fight_option_btn.clicked:
            return utils.sceneValues.fight_scene
        return utils.sceneValues.FOTM_Scene

    def shouldQuit(self) -> bool:
        return self.quit_btn.clicked
