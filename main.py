import cv2 as cv

from save_load import load_save_file
from scenes.ShopScene import ShopScene
from scenes.main_scene import MainScene
from scenes.FightOrTrainMenuScene import FightOrTrainMenuScene
from scenes.FightScene import FightScene
from scenes.TrainScene import TrainScene
from globals import width, height

cap = cv.VideoCapture(0)
cap.set(cv.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, height)

# To add a new scene, add it here and also add it in the scene value place so that scenes don't break
all_scenes = [MainScene(), FightOrTrainMenuScene(), FightScene(), ShopScene(), TrainScene()]
curr_scene_idx = 0
p_idx = curr_scene_idx

load_save_file()

while True:
    _, img = cap.read()
    img = cv.flip(img, 1)

    curr_scene = all_scenes[curr_scene_idx]

    if curr_scene_idx != p_idx:
        curr_scene.re_init()

    p_idx = curr_scene_idx
    # !! Always keep the update before draw
    curr_scene_idx = curr_scene.update(img) # The update method will return an integer, which is the index

    curr_scene.draw(img)

    cv.imshow("Motion Masher", img)

    if cv.waitKey(1) & 0xFF == ord('q') or curr_scene.shouldQuit():
        break

cap.release()
cv.destroyAllWindows()
