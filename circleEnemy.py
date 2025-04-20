import time

import cv2 as cv

import playerStats
from globals import hand_utils


class CircleEnemy:
    def __init__(self, x, y, health, colour):
        self.HEALTH_TO_RADIUS = 10

        self.x = x
        self.y = y
        self.health = health
        self.colour = colour
        self.prev_hit_time = 0
        self.complete_attack_ready = False # If the player opened their hands after attacking, so that a complete attack may be processed

    def draw(self, img):
        if self.health > 0:
            cv.circle(img, (self.x, self.y), self.health * self.HEALTH_TO_RADIUS, self.colour, -1)

    def update(self, hand_closed):
        """

        :param hand_closed:
        :return: change in health
        """
        if self.health > 0:
            if not hand_closed:
                self.complete_attack_ready = True
            t = time.time()
            if self.is_colliding_with_hand() and hand_closed:
                dmg = 0
                if self.complete_attack_ready:
                    dmg = playerStats.complete_attack_damage
                elif t-self.prev_hit_time >= playerStats.passive_attack_cooldown:
                    dmg = playerStats.passive_attack_damage

                pHealth = self.health
                if dmg != 0:
                    playerStats.money += playerStats.money_per_hit * self.health * dmg # add money the the player which the player popped, into the amount of damage, as a bonus. Gives some extra cash, but thats ok
                    self.health -= dmg
                    self.prev_hit_time = time.time()

                return -1 * min(pHealth, dmg)
        return 0

    def is_colliding_with_hand(self):
        cx, cy = hand_utils.palm_centre
        r = playerStats.attack_radius

        return (self.x-cx)**2 + (self.y - cy)**2 <= (self.HEALTH_TO_RADIUS * self.health + r) ** 2
