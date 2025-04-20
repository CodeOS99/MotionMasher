import cv2 as cv
import random
import time

import playerStats
import utils.sceneValues
from globals import hand_utils, width, height
from utils.UI.button import Button
from utils.counter import Counter

# Basically a watered down version of the circleEnemy
class CircleTarget:
    def __init__(self):
        # Random position within viewable area (with margins)
        self.x = random.randint(100, width - 100)
        self.y = random.randint(100, height - 100)

        # Random size between 30 and 60 pixels radius
        self.radius = random.randint(30, 60)

        # Random color
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        # State
        self.active = True
        self.spawn_time = time.time()

    def draw(self, img):
        cv.circle(img, (self.x, self.y), self.radius, self.color, -1)  # Filled circle
        cv.circle(img, (self.x, self.y), self.radius, (255, 255, 255), 2)  # White border

    def check_hit(self, x, y):
        if not self.active:
            return False

        # Calculate distance between hand and target center
        distance = ((self.x - x) ** 2 + (self.y - y) ** 2) ** 0.5
        return distance <= self.radius


class TrainScene:
    def __init__(self):
        self.back_button = Button(50, 50, 150, 50, (0, 0, 255), "Back")

        # Game stats
        self.targets_hit = 0
        self.accuracy = 0
        self.total_attempts = 0

        # Target management
        self.targets = []
        self.max_targets = 3
        self.target_spawn_timer = Counter(time.time())
        self.spawn_interval = 2.0  # Seconds between spawns

        # Hit detection cooldown
        self.hit_cooldown = False
        self.cooldown_timer = Counter(time.time())
        self.cooldown_duration = 0.5  # Seconds

        # Last hand position
        self.last_hand_pos = (0, 0)

    def draw(self, img):
        # Draw all active targets
        for target in self.targets:
            if target.active:
                target.draw(img)

        # Draw UI elements
        self.back_button.draw(img)

        # Draw stats
        cv.putText(img, f"Targets Hit: {self.targets_hit}", (width - 250, 50),
                   cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

        if self.total_attempts > 0:
            acc_text = f"Accuracy: {(self.targets_hit / self.total_attempts * 100):.1f}%"
            cv.putText(img, acc_text, (width - 250, 130),
                       cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

        # Draw hand position
        cv.circle(img, hand_utils.palm_centre, 10, (0, 255, 255), -1)

        # Draw instructions
        cv.putText(img, "Hit the targets with your hand!", (50, height - 50),
                   cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    def re_init(self):
        # Reset game stats
        self.targets_hit = 0
        self.accuracy = 0
        self.total_attempts = 0

        # Reset target management
        self.targets = []
        self.hit_cooldown = False

        # Reset timers
        self.target_spawn_timer.reset(time.time())
        self.cooldown_timer.reset(time.time())

    def update(self, img):
        # Process image for hand tracking
        imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        hand_closed = hand_utils.open_or_closed(imgRGB, img)

        # Update back button
        self.back_button.update(img)
        if self.back_button.clicked:
            return utils.sceneValues.main_scene

        current_time = time.time()

        # Get hand position
        hand_x, hand_y = hand_utils.palm_centre

        # Spawn new targets if needed
        self.target_spawn_timer.update(current_time)
        if len([t for t in self.targets if t.active]) < self.max_targets and self.target_spawn_timer.has_passed(
                self.spawn_interval):
            self.targets.append(CircleTarget())
            self.target_spawn_timer.reset(current_time)

        # Update cooldown
        if self.hit_cooldown:
            self.cooldown_timer.update(current_time)
            if self.cooldown_timer.has_passed(self.cooldown_duration):
                self.hit_cooldown = False

        # Check for hits if hand is closed
        if hand_closed and not self.hit_cooldown:
            hit_detected = False
            self.total_attempts += 1

            for target in self.targets:
                if target.active and target.check_hit(hand_x, hand_y):
                    target.active = False
                    self.targets_hit += 1
                    hit_detected = True

                    # Add visual feedback for hit
                    cv.circle(img, (target.x, target.y), target.radius + 10, (0, 255, 0), 3)

                    numOfStatsToIncrease = random.randint(1, 3)
                    if numOfStatsToIncrease >= 1:
                        playerStats.attack_radius += 1
                    if numOfStatsToIncrease >= 2:
                        playerStats.passive_attack_cooldown -= 0.01
                    if numOfStatsToIncrease >= 3:
                        playerStats.money += 10

            # Start cooldown after attempt
            self.hit_cooldown = True
            self.cooldown_timer.reset(current_time)

            # Visual feedback for miss
            if not hit_detected:
                cv.circle(img, (hand_x, hand_y), 30, (0, 0, 255), 3)

        # Remove old inactive targets 
        self.targets = [t for t in self.targets if t.active or (current_time - t.spawn_time) < 1.0]

        # Store hand position for next frame
        self.last_hand_pos = (hand_x, hand_y)

        return utils.sceneValues.train_scene

    def shouldQuit(self):
        return False