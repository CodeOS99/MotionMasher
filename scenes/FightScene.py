import time

import numpy as np

import playerStats
import utils.sceneValues
from circleEnemy import CircleEnemy
from globals import hand_utils, width, height, mpDraw
from utils.counter import Counter
import cv2 as cv

class FightScene:
    def __init__(self):
        self.prev_lmks = []
        self.circles = [] # List of circle enemies to be drawn on the screen
        self.previously_open = False
        self.counters = {
            "circle_spawner": Counter(0)
        }

    def draw(self, img):
        imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        self.previously_open = hand_utils.open_or_closed(imgRGB, img)

        # Display the amount of money
        cv.putText(img, f"Money: {playerStats.money}", (10, 50), cv.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2)

        cv.circle(img, hand_utils.palm_centre, playerStats.attack_radius, (0, 255, 0), 2)
        for circle in self.circles:
            circle.draw(img)

    def update(self, img) -> int:
        for counter in self.counters.values():
            counter.update(time.time())

        if self.counters["circle_spawner"].has_passed(1):
            self._spawn_circle_enemy()
            self.counters["circle_spawner"].reset(time.time())

        for circle in self.circles:
            circle.update(self.previously_open)

        return utils.sceneValues.fight_scene

    def _spawn_circle_enemy(self):
        x = np.random.randint(100, width-100)
        y = np.random.randint(100, height-100)
        health = np.random.randint(1, 5)
        colour = (np.random.randint(0, 255), np.random.randint(0, 255), np.random.randint(0, 255))
        self.circles.append(CircleEnemy(x, y, health, colour))

    def shouldQuit(self) -> bool:
         return False
