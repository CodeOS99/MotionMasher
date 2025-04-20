import time

import playerStats
import utils.colours
from globals import width, height
from utils.UI.button import Button
from utils.sceneValues import shop_scene
import cv2 as cv
from globals import hand_utils

"""attack_radius = 15
passive_attack_damage = 1
passive_attack_cooldown = 0.5
complete_attack_damage = 2
money = 0
money_per_hit = 1
max_enemy_power = 50"""


class ShopScene:
    def __init__(self):
        # Row 1
        self.active_attack_damage_btn = Button(1/8 * width, 3/8 * height, 275, 50, utils.colours.orange, "Active Attack Damage")
        self.passive_attack_damage_btn = Button(3/8 * width + 100, 3/8 * height, 275, 50, utils.colours.orange, "Passive Attack Damage")
        self.passive_attack_cooldown_btn = Button(5/8 * width + 200, 3/8 * height, 275, 50, utils.colours.orange, "Passive Attack Cooldown")

        # Row 2
        self.attack_radius_btn = Button(1/8 * width, 5/8 * height, 275, 50, utils.colours.orange, "Attack Radius")
        self.money_per_hit_btn = Button(3/8 * width + 100, 5/8 * height, 275, 50, utils.colours.orange, "Money per Hit")
        self.max_enemy_power_btn = Button(5/8 * width + 200, 5/8 * height, 275, 50, utils.colours.orange, "Max Enemy Power")

        # Meta buttons
        self.back_option_btn = Button(width - 500, height-100, 200, 100, utils.colours.purple, "Back")
        self.quit_btn = Button(width-200, height-100, 200, 100, utils.colours.red, "QUIT")

        self.buttons = (
            self.active_attack_damage_btn,
            self.passive_attack_damage_btn,
            self.passive_attack_cooldown_btn,
            self.attack_radius_btn,
            self.money_per_hit_btn,
            self.max_enemy_power_btn,
            self.back_option_btn,
            self.quit_btn
        )

        self.active_attack_damage_cost = 100
        self.passive_attack_damage_cost = 50
        self.passive_attack_cooldown_cost = 75
        self.attack_radius_cost = 40
        self.money_per_hit_cost = 150
        self.max_enemy_power_cost = 65
        self.cost_scaling = 1.25

        self.should_quit = False

        self.about_text = "About: "
        self.cost_text = "Cost: "
        self.prev_clicked = False

        self.last_purchase_time = time.time() # Timer
        self.purchase_cooldown = 0.5

    def draw(self, img):
        for button in self.buttons:
            button.draw(img)

        cv.putText(img, self.about_text, (200, 50), cv.FONT_HERSHEY_PLAIN, 2, utils.colours.black, 2)
        cv.putText(img, self.cost_text, (200, 150), cv.FONT_HERSHEY_PLAIN, 2, utils.colours.black, 2)
        # Put money in the bottom left corner
        cv.putText(img, f"Money: {playerStats.money}", (10, height - 50), cv.FONT_HERSHEY_PLAIN, 2, utils.colours.black, 2)
        imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        self.prev_clicked = hand_utils.open_or_closed(imgRGB, img)

    def re_init(self):
        pass

    def update(self, img):
        for button in self.buttons:
            button.update(img)

        imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        boughtSomething = False
        if self.active_attack_damage_btn.hovered(imgRGB):
            self.about_text = "About: Increases the damage of your active attack."
            self.cost_text = f"Cost: {self.active_attack_damage_cost}"

            if self.prev_clicked:
                if playerStats.money >= self.active_attack_damage_cost and time.time()-self.last_purchase_time >= self.purchase_cooldown:
                    playerStats.complete_attack_damage += 1
                    playerStats.money -= self.active_attack_damage_cost
                    self.active_attack_damage_cost = int(self.active_attack_damage_cost * self.cost_scaling)
                    boughtSomething = True
                else:
                    self.about_text = "Not enough money!"

        elif self.passive_attack_damage_btn.hovered(imgRGB):
            self.about_text = "About: Increases the damage of your passive attack."
            self.cost_text = f"Cost: {self.passive_attack_damage_cost}"

            if self.prev_clicked:
                if playerStats.money >= self.passive_attack_damage_cost and time.time()-self.last_purchase_time >= self.purchase_cooldown:
                    playerStats.passive_attack_damage += 1
                    playerStats.money -= self.passive_attack_damage_cost
                    self.passive_attack_damage_cost = int(self.passive_attack_damage_cost * self.cost_scaling)
                    boughtSomething = True
                else:
                    self.about_text = "Not enough money!"

        elif self.passive_attack_cooldown_btn.hovered(imgRGB):
            self.about_text = "About: Decreases the cooldown of your passive attack."
            self.cost_text = f"Cost: {self.passive_attack_cooldown_cost}"

            if self.prev_clicked:
                if playerStats.money >= self.passive_attack_cooldown_cost and time.time()-self.last_purchase_time >= self.purchase_cooldown:
                    playerStats.passive_attack_cooldown -= 0.1
                    playerStats.money -= self.passive_attack_cooldown_cost
                    self.passive_attack_cooldown_cost = int(self.passive_attack_cooldown_cost * self.cost_scaling)
                    boughtSomething = True
                else:
                    self.about_text = "Not enough money!"

        elif self.attack_radius_btn.hovered(imgRGB):
            self.about_text = "About: Increases the radius of your attack."
            self.cost_text = f"Cost: {self.attack_radius_cost}"

            if self.prev_clicked:
                if playerStats.money >= self.attack_radius_cost and time.time()-self.last_purchase_time >= self.purchase_cooldown:
                    playerStats.attack_radius += 5
                    playerStats.money -= self.attack_radius_cost
                    self.attack_radius_cost = int(self.attack_radius_cost * self.cost_scaling)
                    boughtSomething = True
                else:
                    self.about_text = "Not enough money!"

        elif self.money_per_hit_btn.hovered(imgRGB):
            self.about_text = "About: Increases the amount of money you get per hit."
            self.cost_text = f"Cost: {self.money_per_hit_cost}"

            if self.prev_clicked:
                if playerStats.money >= self.money_per_hit_cost and time.time()-self.last_purchase_time >= self.purchase_cooldown:
                    playerStats.money_per_hit += 1
                    playerStats.money -= self.money_per_hit_cost
                    self.money_per_hit_cost = int(self.money_per_hit_cost * self.cost_scaling)
                    boughtSomething = True
                else:
                    self.about_text = "Not enough money!"

        elif self.max_enemy_power_btn.hovered(imgRGB):
            self.about_text = "About: Increases the maximum enemy power."
            self.cost_text = f"Cost: {self.max_enemy_power_cost}"

            if self.prev_clicked:
                if playerStats.money >= self.max_enemy_power_cost and time.time()-self.last_purchase_time >= self.purchase_cooldown:
                    playerStats.max_enemy_power += 5
                    playerStats.money -= self.max_enemy_power_cost
                    self.max_enemy_power_cost = int(self.max_enemy_power_cost * self.cost_scaling)
                    boughtSomething = True
                else:
                    self.about_text = "Not enough money!"

        else:
            self.about_text = "About: "
            self.cost_text = "Cost: "

        if boughtSomething:
            self.last_purchase_time = time.time()

        if self.back_option_btn.clicked:
            return utils.sceneValues.FOTM_Scene
        elif self.quit_btn.clicked:
            self.should_quit = True
        return shop_scene

    def shouldQuit(self):
        return self.should_quit
