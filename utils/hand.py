import cv2 as cv
import mediapipe as mp
import numpy as np

def calculate_distance(p1, p2):
    return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

class HandUtils:
    def __init__(self, tracker, drawing_utils):
        if tracker is None or drawing_utils is None:
            raise ValueError("Tracker and drawing_utils must be provided.")

        self.tracker = tracker
        self.drawing_utils = drawing_utils
        self.finger_tips = []
        self.palm_centre = (-50, -50)
        self.avg_palm_radius = 0

        self.HANDS = {
            "THUMB": 0,
            "INDEX": 1,
            "MIDDLE": 2,
            "RING": 3,
            "PINKY": 4
        }
        self._FINGERTIP_LANDMARKS = [4, 8, 12, 16, 20] # Correct indices for fingertips

    def _get_landmarks(self, imgRGB):
        results = self.tracker.process(imgRGB)
        return results.multi_hand_landmarks

    def _calculate_scaled_coords(self, landmark, img_width, img_height):
        # This helper remains the same, scaling based on provided dimensions
        return (int(landmark.x * img_width), int(landmark.y * img_height))

    def open_or_closed(self, imgRGB, draw_img=None):
        # --- Get actual image dimensions ---
        img_height, img_width, _ = imgRGB.shape
        all_hands_landmarks = self._get_landmarks(imgRGB)

        if all_hands_landmarks:
            for multi_hand_landmark in all_hands_landmarks:
                primary_hand_landmarks = multi_hand_landmark.landmark
                # --- Use actual image dimensions for scaling ---
                self.finger_tips = [
                    self._calculate_scaled_coords(primary_hand_landmarks[tip_idx], img_width, img_height)
                    for tip_idx in self._FINGERTIP_LANDMARKS
                ]

                # --- Use actual image dimensions for scaling ---
                wrist_coord = self._calculate_scaled_coords(primary_hand_landmarks[0], img_width, img_height)
                middle_mcp_coord = self._calculate_scaled_coords(primary_hand_landmarks[9], img_width, img_height)

                self.palm_centre = (
                    (wrist_coord[0] + middle_mcp_coord[0]) // 2,
                    (wrist_coord[1] + middle_mcp_coord[1]) // 2
                )

                fingertip_distances = [
                    calculate_distance(tip_coord, self.palm_centre)
                    for tip_coord in self.finger_tips
                ]

                self.avg_palm_radius = calculate_distance(wrist_coord, middle_mcp_coord) * 1.2

                if draw_img is not None:
                    # Ensure draw_img has the same dimensions as imgRGB for circles to align perfectly
                    # If draw_img is a different size, mpDraw will scale to it, but cv.circles might seem off.
                    draw_height, draw_width, _ = draw_img.shape
                    if draw_width != img_width or draw_height != img_height:
                        # Optional: Add a warning or resize draw_img if needed
                        print("Warning: draw_img dimensions differ from imgRGB. Manual drawings might not align perfectly with mpDraw.")

                    # mpDraw scales internally based on draw_img dimensions
                    self.drawing_utils.draw_landmarks(draw_img, all_hands_landmarks[0], mp.solutions.hands.HAND_CONNECTIONS)

                    # cv.circle uses coordinates scaled based on imgRGB dimensions
                    cv.circle(draw_img, wrist_coord, 5, (0, 255, 0), -1)
                    cv.circle(draw_img, middle_mcp_coord, 5, (0, 0, 255), -1)
                    cv.circle(draw_img, self.palm_centre, 7, (255, 0, 0), -1)


                all_fingers_close = all(dist < self.avg_palm_radius for dist in fingertip_distances)

                thumb_to_index_dist = calculate_distance(
                    self.finger_tips[self.HANDS["THUMB"]],
                    self.finger_tips[self.HANDS["INDEX"]]
                )
                thumb_near_index_and_others_close = (
                    thumb_to_index_dist < 50 and
                    fingertip_distances[self.HANDS["INDEX"]] < self.avg_palm_radius and
                    fingertip_distances[self.HANDS["MIDDLE"]] < self.avg_palm_radius and
                    fingertip_distances[self.HANDS["RING"]] < self.avg_palm_radius
                )

                is_closed = all_fingers_close or thumb_near_index_and_others_close
                return is_closed

        else:
            self.avg_palm_radius = 0
            self.finger_tips = []
            self.palm_centre = (-50, -50)
            return False

    def get_palm_centers(self, imgRGB):
        # --- Get actual image dimensions ---
        img_height, img_width, _ = imgRGB.shape
        all_hands_landmarks = self._get_landmarks(imgRGB)
        palm_centres = []

        if all_hands_landmarks:
            for hand_landmarks in all_hands_landmarks:
                landmarks = hand_landmarks.landmark

                # --- Use actual image dimensions for scaling ---
                wrist_coord = self._calculate_scaled_coords(landmarks[0], img_width, img_height)
                middle_mcp_coord = self._calculate_scaled_coords(landmarks[9], img_width, img_height)

                center = (
                    (wrist_coord[0] + middle_mcp_coord[0]) // 2,
                    (wrist_coord[1] + middle_mcp_coord[1]) // 2
                )
                palm_centres.append(center)

        return palm_centres

    def get_palm_radius(self, imgRGB):
        # --- Get actual image dimensions ---
        img_height, img_width, _ = imgRGB.shape
        all_hands_landmarks = self._get_landmarks(imgRGB)
        palm_radii = []

        if all_hands_landmarks:
            for hand_landmarks in all_hands_landmarks:
                landmarks = hand_landmarks.landmark

                # --- Use actual image dimensions for scaling ---
                wrist_coord = self._calculate_scaled_coords(landmarks[0], img_width, img_height)
                middle_mcp_coord = self._calculate_scaled_coords(landmarks[9], img_width, img_height)

                radius = calculate_distance(wrist_coord, middle_mcp_coord) * 1.2
                palm_radii.append(radius)

        return palm_radii

    def update_fingertips_pos(self, imgRGB):
        all_hands_landmarks = self._get_landmarks(imgRGB)

        if all_hands_landmarks:
            primary_hand_landmarks = all_hands_landmarks[0].landmark
            img_height, img_width, _ = imgRGB.shape

            self.finger_tips = [
                self._calculate_scaled_coords(primary_hand_landmarks[tip_idx], img_width, img_height)
                for tip_idx in self._FINGERTIP_LANDMARKS
            ]
            return True
        else:
            self.finger_tips = []
            return False