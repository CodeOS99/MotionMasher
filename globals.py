width = 1080
height = 720

from utils.hand import HandUtils
import mediapipe as mp

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

hand_utils = HandUtils(hands, mpDraw)
