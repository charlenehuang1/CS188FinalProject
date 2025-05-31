import cv2 
import mediapipe as mp
import numpy as np
import socket
import pickle
from server import send, connect

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 600)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 400)

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
                send(hand_landmarks)
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        cv2.imshow("Hand Tracking", frame)
        if cv2.waitKey(1) == ord('q'):
            break


def get_hand_orientation(landmarks):
    wrist = np.array([landmarks[0].x, landmarks[0].y, landmarks[0].z])
    index_mcp = np.array([landmarks[5].x, landmarks[5].y, landmarks[5].z])
    pinky_mcp = np.array([landmarks[17].x, landmarks[17].y, landmarks[17].z])

    x_axis = index_mcp - wrist
    x_axis /= np.linalg.norm(x_axis)

    y_axis = pinky_mcp - wrist
    y_axis /= np.linalg.norm(y_axis)

    z_axis = np.cross(x_axis, y_axis)
    z_axis /= np.linalg.norm(z_axis)

    y_axis = np.cross(z_axis, x_axis)  # Re-orthogonalize

    # Create rotation matrix (column-wise)
    R = np.column_stack((x_axis, y_axis, z_axis))
    return R  # 3x3 rotation matrix


cv2.destroyAllWindows()
