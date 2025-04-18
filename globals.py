width = 1080
height = 720

from utils.hand import HandUtils
import mediapipe as mp

mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=2)
mpDraw = mp.solutions.drawing_utils

hand_utils = HandUtils(hands, mpDraw)
