import time

import cv2 as cv

import playerStats
from globals import hand_utils, mpHands


class CircleEnemy:
    def __init__(self, x, y, health, colour):
        self.HEALTH_TO_RADIUS = 10

        self.x = x
        self.y = y
        self.health = health
        self.colour = colour
        self.prev_hit_time = 0

    def draw(self, img):
        if self.health > 0:
            cv.circle(img, (self.x, self.y), self.health * self.HEALTH_TO_RADIUS, self.colour, -1)

    def update(self, hand_closed):
        if self.health > 0:
            t = time.time()
            if self.is_colliding_with_hand() and hand_closed and t - self.prev_hit_time > 0.5: # is colliding, closed, and a .5s cooldown
                playerStats.money += playerStats.money_per_hit * self.health
                self.health -= playerStats.attack_damage
                self.prev_hit_time = time.time()

    def is_colliding_with_hand(self):
        cx, cy = hand_utils.palm_centre
        r = playerStats.attack_radius

        return (self.x-cx)**2 + (self.y - cy)**2 <= (self.HEALTH_TO_RADIUS * self.health + r) ** 2
