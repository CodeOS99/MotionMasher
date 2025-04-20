import utils.sceneValues
from save_load import save_game
from utils.UI.button import Button
from utils.colours import *
from globals import hand_utils, width, height
import cv2 as cv
import time


class MainScene:
    def __init__(self):
        """
        This scene has 2 buttons, one to start, and one to quit. the draw function draws both of them and the update function calls update on the buttons, which in turn checks for the cursor hovering or clicking and also the update function updates the coords of the hands class
        """
        self.startBtn: Button = Button(width // 2, height // 2 - 120, 200, 100, blue, "START")
        self.saveBtn: Button = Button(width // 2, height // 2, 200, 100, green, "SAVE GAME")
        self.quitBtn: Button = Button(width // 2, height // 2 + 120, 200, 100, red, "QUIT")

        self.BUTTONS = (self.startBtn, self.saveBtn, self.quitBtn)
        self.init_time = time.time()
        self.init_timer_lim = 1
        self.save_message = ""
        self.save_message_time = 0

    def draw(self, img) -> None:
        for btn in self.BUTTONS:
            btn.draw(img)

        cv.putText(img, "MOTION MASHER!", (70, 150), cv.FONT_HERSHEY_PLAIN, 7, black, 2)

        # Update hand tracking
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
        # Show save message if active
        if time.time() - self.save_message_time < 2 and self.save_message:
            cv.putText(img, self.save_message,
                       (width // 2 - 100, height - 50),
                       cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    def re_init(self):
        self.init_time = time.time()

    def update(self, img) -> int:
        imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        buffer_active = time.time() - self.init_time < self.init_timer_lim

        # Only update buttons if buffer time has passed
        if not buffer_active:
            for btn in self.BUTTONS:
                btn.update(imgRGB)

            # Track hand position but don't use for clicks during buffer
            _ = hand_utils.open_or_closed(imgRGB)

            if self.startBtn.clicked:
                return utils.sceneValues.FOTM_Scene

            if self.saveBtn.clicked:
                save_game()
                self.save_message = "GAME SAVED"
                self.save_message_time = time.time()

        return utils.sceneValues.main_scene

    def shouldQuit(self) -> bool:
        # Only allow quitting if buffer time has passed
        if time.time() - self.init_time < self.init_timer_lim:
            return False
        return self.quitBtn.clicked