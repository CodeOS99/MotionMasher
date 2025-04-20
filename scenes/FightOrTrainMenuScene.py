import time

import cv2 as cv

import utils.sceneValues
from utils.UI.button import Button
from utils.colours import *
from globals import hand_utils, width, height


class FightOrTrainMenuScene:
    # FOTM_Scene
    def __init__(self):
        self.fight_option_btn = Button(2/8 * width, height/2 - 90, 200, 100, orange, "FIGHT!")
        self.back_option_btn = Button(0, 0, 200, 100, purple, "Back")
        self.train_option_btn = Button(4/8 * width, height/2 - 90, 200, 100, green, "TRAIN!")
        self.shop_option_btn = Button(6/8 * width, height/2-90, 200, 100, cyan, "SHOP!")
        self.quit_btn = Button(width-200, height-100, 200, 100, red, "QUIT")

        self.BUTTONS = (self.fight_option_btn, self.back_option_btn, self.train_option_btn, self.shop_option_btn, self.quit_btn)
        self.init_time = time.time()

        self.init_timer_lim = 1

    def re_init(self):
        self.init_time = time.time()

    def update(self, img) -> int:
        imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        buffer_active = time.time() - self.init_time < self.init_timer_lim

        # Only update buttons if buffer time has passed
        if not buffer_active:
            for btn in self.BUTTONS:
                btn.update(imgRGB)

            if self.back_option_btn.clicked:
                return utils.sceneValues.main_scene
            if self.fight_option_btn.clicked:
                return utils.sceneValues.fight_scene
            if self.train_option_btn.clicked:
                return utils.sceneValues.train_scene
            if self.shop_option_btn.clicked:
                return utils.sceneValues.shop_scene

        return utils.sceneValues.FOTM_Scene

    def draw(self, img) -> None:
        # Draw all buttons
        for btn in self.BUTTONS:
            btn.draw(img)

        imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        hand_utils.open_or_closed(imgRGB, img)

        # Show buffer countdown
        buffer_active = time.time() - self.init_time < self.init_timer_lim
        if buffer_active:
            # Create semi-transparent overlay
            overlay = img.copy()
            cv.rectangle(overlay, (0, 0), (len(img[0]), height), (0, 0, 0), -1)
            cv.addWeighted(overlay, 0.3, img, 0.7, 0, img)

            # Show countdown timer
            seconds_left = max(0, self.init_timer_lim - int(time.time() - self.init_time))
            cv.putText(img, f"Starting in {seconds_left}...",
                       (width // 2 - 150, height // 2),
                       cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    def shouldQuit(self) -> bool:
        return self.quit_btn.clicked
