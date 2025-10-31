import cv2
import mediapipe as mp
import pyautogui
import random
import numpy as np
from PIL import ImageGrab  # for screenshots

screen_width, screen_height = pyautogui.size()

mpHands = mp.solutions.hands
hands = mpHands.Hands(
    static_image_mode=False,
    model_complexity=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7,
    max_num_hands=1
)

# ---------------- Utility Functions ----------------

def get_angle(a, b, c):
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(np.degrees(radians))
    return angle

def get_distance(landmark_list):
    if len(landmark_list) < 2:
        return 0
    (x1, y1), (x2, y2) = landmark_list[0], landmark_list[1]
    return np.hypot(x2 - x1, y2 - y1) * 1000  # scale distance

def find_finger_tip(processed):
    if processed.multi_hand_landmarks:
        hand_landmarks = processed.multi_hand_landmarks[0]
        index_tip = hand_landmarks.landmark[mpHands.HandLandmark.INDEX_FINGER_TIP]
        return index_tip
    return None

def move_mouse(index_finger_tip):
    if index_finger_tip:
        x = int(index_finger_tip.x * screen_width)
        y = int(index_finger_tip.y * screen_height / 2)
        pyautogui.moveTo(x, y)

# ---------------- Gesture Conditions ----------------

def is_left_click(landmarks, thumb_index_dist):
    return (
        get_angle(landmarks[5], landmarks[6], landmarks[8]) < 50 and
        get_angle(landmarks[9], landmarks[10], landmarks[12]) > 90 and
        thumb_index_dist > 50
    )

def is_right_click(landmarks, thumb_index_dist):
    return (
        get_angle(landmarks[9], landmarks[10], landmarks[12]) < 50 and
        get_angle(landmarks[5], landmarks[6], landmarks[8]) > 90 and
        thumb_index_dist > 50
    )

def is_double_click(landmarks, thumb_index_dist):
    return (
        get_angle(landmarks[5], landmarks[6], landmarks[8]) < 50 and
        get_angle(landmarks[9], landmarks[10], landmarks[12]) < 50 and
        thumb_index_dist > 50
    )

def is_screenshot(landmarks, thumb_index_dist):
    return (
        get_angle(landmarks[5], landmarks[6], landmarks[8]) < 50 and
        get_angle(landmarks[9], landmarks[10], landmarks[12]) < 50 and
        thumb_index_dist < 50
    )

# ---------------- Main Gesture Detection ----------------

def detect_gesture(frame, landmark_list, processed):
    if len(landmark_list) < 21:
        return

    index_tip = find_finger_tip(processed)
    thumb_index_dist = get_distance([landmark_list[4], landmark_list[5]])

    # Mouse movement (index finger straight + thumb close)
    if thumb_index_dist < 50 and get_angle(landmark_list[5], landmark_list[6], landmark_list[8]) > 90:
        move_mouse(index_tip)

    # Left Click
    elif is_left_click(landmark_list, thumb_index_dist):
        pyautogui.click(button='left')
        cv2.putText(frame, "Left Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Right Click
    elif is_right_click(landmark_list, thumb_index_dist):
        pyautogui.click(button='right')
        cv2.putText(frame, "Right Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Double Click
    elif is_double_click(landmark_list, thumb_index_dist):
        pyautogui.doubleClick()
        cv2.putText(frame, "Double Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

    # Screenshot Gesture
    elif is_screenshot(landmark_list, thumb_index_dist):
        label = random.randint(1, 1000)
        img = ImageGrab.grab()
        img.save(f'screenshot_{label}.png')
        cv2.putText(frame, "Screenshot Taken", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

# ---------------- Main Function ----------------

def main():
    draw = mp.solutions.drawing_utils
    cap = cv2.VideoCapture(0)

    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.flip(frame, 1)
            frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            processed = hands.process(frameRGB)

            landmark_list = []
            if processed.multi_hand_landmarks:
                hand_landmarks = processed.multi_hand_landmarks[0]
                draw.draw_landmarks(frame, hand_landmarks, mpHands.HAND_CONNECTIONS)
                for lm in hand_landmarks.landmark:
                    landmark_list.append((lm.x, lm.y))

            detect_gesture(frame, landmark_list, processed)

            cv2.imshow('Virtual Mouse', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
