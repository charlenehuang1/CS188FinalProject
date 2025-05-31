import cv2
import mediapipe as mp
import numpy as np
import robosuite as suite


# === Robosuite Setup ===

env = suite.make(
    env_name="Lift",
    robots="Panda",
    controller_configs=controller_config,
    has_renderer=True,
    use_camera_obs=False,
    control_freq=20,
)

obs = env.reset()

# === MediaPipe Setup ===
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

# === Helper Function ===
def map_landmark_to_action(x, y, grip_dist):
    """
    Map MediaPipe index fingertip position and grip distance to robot action.
    """
    dx = (x - 0.5) * 0.2    # range approx [-0.1, 0.1]
    dy = (0.5 - y) * 0.2    # invert y
    dz = 0.0                # fixed z for simplicity

    # Gripper: -1.0 = closed, 1.0 = open
    gripper = -1.0 if grip_dist < 0.05 else 1.0

    return [dx, dy, dz, gripper]

print("Use your index finger to move the robot and pinch thumb+index to close gripper.")
print("Press 'q' to quit.")

# === Main Loop ===
while True:
    ret, frame = cap.read()
    if not ret:
        continue

    # Process frame for hand tracking
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    action = [0.0, 0.0, 0.0, 1.0]  # Default: no movement, gripper open

    if results.multi_hand_landmarks:
        hand_landmarks = results.multi_hand_landmarks[0]

        # Get normalized coordinates of index tip and thumb tip
        index_tip = hand_landmarks.landmark[8]
        thumb_tip = hand_landmarks.landmark[4]

        # Compute grip distance (Euclidean)
        grip_dist = np.sqrt((index_tip.x - thumb_tip.x)**2 + (index_tip.y - thumb_tip.y)**2)

        # Map index finger to x, y movement, thumb distance to gripper
        action = map_landmark_to_action(index_tip.x, index_tip.y, grip_dist)

        # Draw landmarks for visualization
        mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Step the Robosuite environment with action
    obs, reward, done, _ = env.step(action)
    env.render()

    # Show webcam feed with landmarks
    cv2.imshow("Hand Tracking", frame)

    # Exit on 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# === Cleanup ===
cap.release()
cv2.destroyAllWindows()
