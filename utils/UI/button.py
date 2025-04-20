import math
import cv2 as cv
from globals import hand_utils
import numpy as np

class Button:
    def __init__(self, x, y, w, h, col, text=""):
        self.x = int(math.floor(x))
        self.y = int(math.floor(y))
        self.w = int(math.floor(w))
        self.h = int(math.floor(h))

        self.init_col = col

        self.hover_col = list(self.init_col)
        self.click_col = list(self.init_col)

        maxVal = 0
        idx = 0
        # Find the idx where the color value is maximum, for automatic colour changing
        for i in range(3):
            if self.init_col[i] > maxVal:
                maxVal = self.init_col[i]
                idx = i

        self.hover_col[idx] //= 2
        self.click_col[idx] //= 4

        self.hover_col = tuple(self.hover_col)
        self.click_col = tuple(self.click_col)

        self.col = self.init_col

        self.hover_radius = 10  # radius of palm detection circle

        self.text = text

        self.clicked = False

    def draw(self, frame):
        cv.rectangle(frame, (self.x, self.y), (self.x+self.w, self.y+self.h), self.col, -1)

        font = cv.FONT_HERSHEY_SIMPLEX
        font_scale = 0.7
        thickness = 2
        text_size, _ = cv.getTextSize(self.text, font, font_scale, thickness)

        text_width, text_height = text_size
        text_x = self.x + (self.w - text_width) // 2
        text_y = self.y + (self.h + text_height) // 2

        cv.putText(frame, self.text, (text_x, text_y), font, font_scale, (255, 255, 255), thickness)

    def update(self, frameRGB):
        cx, cy = hand_utils.palm_centre
        r = self.hover_radius

        # Clamp the palm centre to the rectangle bounds to find closest point
        closest_x = max(self.x, min(cx, self.x + self.w))
        closest_y = max(self.y, min(cy, self.y + self.h))

        # Distance from palm centre to the closest point on the rectangle
        dist = math.hypot(cx - closest_x, cy - closest_y)

        if dist < r:
            self.col = self.hover_col
        else:
            self.col = self.init_col

        if hand_utils.open_or_closed(frameRGB) and dist < r:
            self.col = self.click_col
            self.clicked = True
        else:
            self.clicked = False

    def hovered(self, frameRGB):
        return self.col == self.hover_col
