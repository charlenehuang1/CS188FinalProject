import cv2 
import mediapipe as mp

cap1 = cv2.VideoCapture(0)
cap2 = cv2.VideoCapture(1)

cap1.set(cv2.CAP_PROP_FRAME_WIDTH, 600)
cap1.set(cv2.CAP_PROP_FRAME_HEIGHT, 400)

cap2.set(cv2.CAP_PROP_FRAME_WIDTH, 600)
cap2.set(cv2.CAP_PROP_FRAME_HEIGHT, 400)


mp_drawing_1 = mp.solutions.drawing_utils 
mp_hands_1 = mp.solutions.hands
hand_1 = mp_hands_1.Hands()


mp_drawing_2 = mp.solutions.drawing_utils 
mp_hands_2 = mp.solutions.hands
hand_2 = mp_hands_2.Hands()

while True: 
    success1, frame1 = cap1.read()
    success2, frame2 = cap2.read()

    if success1: 
        RGB_frame = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)
        result = hand_1.process(frame1)
        if result.multi_hand_landmarks: 
            for hand_landmarks in result.multi_hand_landmarks: 
                print(hand_landmarks)
                mp_drawing_1.draw_landmarks(frame1, hand_landmarks, mp_hands_1.HAND_CONNECTIONS)
        cv2.imshow("Hand Tracking 1", frame1)
        if cv2.waitKey(1) == ord('q'):
            break

    if success2: 
        RGB_frame = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)
        result = hand_2.process(frame2)
        if result.multi_hand_landmarks: 
            for hand_landmarks in result.multi_hand_landmarks: 
                print(hand_landmarks)
                mp_drawing_2.draw_landmarks(frame2, hand_landmarks, mp_hands_2.HAND_CONNECTIONS)
        cv2.imshow("Hand Tracking 2", frame2)
        if cv2.waitKey(1) == ord('p'):
            break




cv2.destroyAllWindows()