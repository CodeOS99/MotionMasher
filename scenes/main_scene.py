import utils.sceneValues
from utils.UI.button import Button
from utils.colours import *
from globals import hand_utils, width, height
import cv2 as cv

class MainScene:
    def __init__(self):
        """
        This scene has 2 buttons, one to start, and one to quit. the draw function draws both of them and the update function calls update on the buttons, which in turn checks for the cursor hovering or clicking and also the update function updates the coords of the hands class
        """
        self.startBtn: Button = Button(width//2, height//2 - 90, 200, 100, blue, "START")
        self.quitBtn: Button = Button(width//2, height//2 + 90, 200, 100, red, "QUIT")

        self.BUTTONS = (self.startBtn, self.quitBtn)

    def draw(self, img) -> None:
        for btn in self.BUTTONS:
            btn.draw(img)

        cv.putText(img, "MOTION MASHER!", (70, 150), cv.FONT_HERSHEY_PLAIN, 7, black, 2)

    def update(self, img) -> int:
        imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)

        for btn in self.BUTTONS:
            btn.update(imgRGB)
        _ = hand_utils.open_or_closed(imgRGB, img)  # in order to update hand's positions on which other things may rely

        if self.startBtn.clicked:
            return utils.sceneValues.FOTM_Scene
        return utils.sceneValues.main_scene

    def shouldQuit(self) -> bool:
        return self.quitBtn.clicked
