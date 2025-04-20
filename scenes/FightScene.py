import time

import numpy as np
from numpy.ma.core import floor

import playerStats
import utils.sceneValues
from circleEnemy import CircleEnemy
from globals import hand_utils, width, height, mpDraw
from utils.UI.button import Button
from utils.counter import Counter
import cv2 as cv

class FightScene:
    def __init__(self):
        self.backButton = Button(width//2 + 100, height//2 + 50, 200, 100, (0, 0, 255), "Back")
        self.prev_lmks = []
        self.circles = [] # List of circle enemies to be drawn on the screen
        self.previously_open = False
        self.counters = {
            "circle_spawner": Counter(0)
        }
        self.total_enemy_power = 0 # Player loses when the cumulative health of the circle enemies(total_enemy_power) is greater than the max enemy power

    def draw(self, img):
        _overlay = img.copy()
        overlay_height = int(floor(self.total_enemy_power / playerStats.max_enemy_power * height))
        cv.rectangle(_overlay, (0, height - overlay_height), (len(img[0]), height), (0, 0, 255), -1)

        # Blend overlay onto original image and modify img in-place
        cv.addWeighted(img, 0.7, _overlay, 0.3, 0, dst=img)

        imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        self.previously_open = hand_utils.open_or_closed(imgRGB, img)

        cv.circle(img, hand_utils.palm_centre, playerStats.attack_radius, (0, 255, 0), 2)
        for circle in self.circles:
            circle.draw(img)

        # Display the amount of money
        cv.putText(img, f"Money: {playerStats.money}", (10, 50), cv.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2)

        if self.total_enemy_power >= playerStats.max_enemy_power:
            cv.putText(img, "GAME OVER!", (width//2 - 100, height//2), cv.FONT_HERSHEY_PLAIN, 7, (0, 0, 0), 2)
            self.backButton.draw(img)

    def update(self, img) -> int:
        if self.total_enemy_power < playerStats.max_enemy_power:
            for counter in self.counters.values():
                counter.update(time.time())

            if self.counters["circle_spawner"].has_passed(1):
                self._spawn_circle_enemy()
                self.counters["circle_spawner"].reset(time.time())

            for circle in self.circles:
                self.total_enemy_power += circle.update(self.previously_open)
        else:
            imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
            self.backButton.update(imgRGB)
            if self.backButton.clicked:
                return utils.sceneValues.main_scene
        return utils.sceneValues.fight_scene

    def _spawn_circle_enemy(self):
        x = np.random.randint(100, width-100)
        y = np.random.randint(100, height-100)
        health = np.random.randint(1, 5)
        colour = (np.random.randint(0, 255), np.random.randint(0, 255), np.random.randint(0, 255))
        self.circles.append(CircleEnemy(x, y, health, colour))
        self.total_enemy_power += health

    def shouldQuit(self) -> bool:
         return False
