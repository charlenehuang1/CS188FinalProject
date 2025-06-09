import cv2 
import mediapipe as mp
import numpy as np
from server import send, connect

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

mp_drawing = mp.solutions.drawing_utils 
mp_hands = mp.solutions.hands
hand = mp_hands.Hands()

connect()

while True:
    success, frame = cap.read()
    if success: 
        RGB_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hand.process(RGB_frame)
        if result.multi_hand_landmarks: 
            for hand_landmarks in result.multi_hand_landmarks: 
                landmarks_array = np.array([np.array([lm.x, lm.y, lm.z]) for lm in hand_landmarks.landmark])
                send(landmarks_array)
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        cv2.imshow("Hand Tracking", frame)
        if cv2.waitKey(1) == ord('q'):
            break


cv2.destroyAllWindows()
