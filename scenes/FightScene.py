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
        self.backButton = Button(width // 2 + 100, height // 2 + 50, 200, 100, (0, 0, 255), "Back")
        self.prev_lmks = []
        self.circles = []  # List of circle enemies to be drawn on the screen
        self.previously_open = False
        self.counters = {
            "circle_spawner": Counter(0),
            "game_timer": Counter(0)
        }
        self.total_enemy_power = 0  # Player loses when the cumulative health of the circle enemies(total_enemy_power) is greater than the max enemy power

        # Difficulty scaling parameters
        self.start_time = time.time()
        self.game_duration = 0  # Tracks how long player has survived in seconds
        self.base_spawn_time = 1.0  # Initial spawn interval
        self.min_spawn_time = 0.3  # Minimum spawn interval (fastest spawn rate)
        self.base_health = [1, 3]  # Initial health range [min, max]
        self.max_health = [2, 8]  # Maximum health range
        self.enemies_spawned = 0
        self.difficulty_level = 1
        self.score = 0

        self.rendered_for_first_time = True

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

        # Display game stats
        cv.putText(img, f"Money: {playerStats.money}", (10, 50), cv.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2)
        cv.putText(img, f"Level: {self.difficulty_level}", (10, 90), cv.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2)
        cv.putText(img, f"Time: {int(self.game_duration)}s", (10, 130), cv.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2)
        cv.putText(img, f"Score: {self.score}", (10, 170), cv.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2)

        if self.total_enemy_power >= playerStats.max_enemy_power:
            cv.putText(img, "GAME OVER!", (width // 2 - 100, height // 2), cv.FONT_HERSHEY_PLAIN, 7, (0, 0, 0), 2)
            self.backButton.draw(img)

    def update(self, img) -> int:
        if self.rendered_for_first_time:
            self.start_time = time.time()
            self.rendered_for_first_time = False
        current_time = time.time()

        if self.total_enemy_power < playerStats.max_enemy_power:
            # Update game duration
            self.game_duration = current_time - self.start_time

            # Update counters
            for counter in self.counters.values():
                counter.update(current_time)

            # Calculate current difficulty level based on time survived
            self.difficulty_level = 1 + int(self.game_duration / 15)  # Increase level every 15 seconds

            # Calculate spawn interval based on difficulty
            spawn_interval = max(
                self.base_spawn_time - (self.difficulty_level * 0.07),
                self.min_spawn_time
            )

            # Spawn enemies at adjusted rate
            if self.counters["circle_spawner"].has_passed(spawn_interval):
                self._spawn_circle_enemy()
                self.enemies_spawned += 1
                self.counters["circle_spawner"].reset(current_time)

            # Process each circle
            circles_to_keep = []
            for circle in self.circles:
                power_change = circle.update(self.previously_open)
                self.total_enemy_power += power_change

                # If circle was killed (negative power_change), increase score
                if power_change < 0 and circle.health <= 0:
                    self.score += abs(power_change) * self.difficulty_level
                    playerStats.money += int(abs(power_change) * (1 + (self.difficulty_level * 0.1)))

                if circle.health > 0:
                    circles_to_keep.append(circle)

            self.circles = circles_to_keep
        else:
            imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
            self.backButton.update(imgRGB)
            if self.backButton.clicked:
                return utils.sceneValues.main_scene
        return utils.sceneValues.fight_scene

    def _spawn_circle_enemy(self):
        x = np.random.randint(100, width - 100)
        y = np.random.randint(100, height - 100)

        # Scale health based on difficulty level
        min_health = min(
            self.base_health[0] + int(self.difficulty_level * 0.2),
            self.max_health[0]
        )
        max_health = min(
            self.base_health[1] + int(self.difficulty_level * 0.5),
            self.max_health[1]
        )

        health = np.random.randint(min_health, max_health + 1)
        colour = (np.random.randint(0, 255), np.random.randint(0, 255), np.random.randint(0, 255))
        self.circles.append(CircleEnemy(x, y, health, colour))
        self.total_enemy_power += health

    def shouldQuit(self) -> bool:
        return False