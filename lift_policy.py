import numpy as np
import robosuite as suite
from client import receive
import socket
from pid import PID
from filterpy.kalman import KalmanFilter

class LiftPolicy(object):
    """
    Policy class to control a robot arm in Robosuite using hand tracking input.
    """
    def __init__(self, obs):
        self.s = socket.socket()
        self.host = socket.gethostname()
        self.port = 3000
        self.s.connect((self.host, self.port))
        self.original_robot_pos = obs['robot0_eef_pos'].copy()
        self.pid = PID(kp=10, ki=0, kd=0, target=self.original_robot_pos)
        self.dt = 0.01

        self.calibrated = False
        self.hand_origin = None
        self.delay = 10
        self.counter = 0

        self.scale = np.array([6, 1, 4])  # Scaling factor between hand movement deltas and robot motion deltas

        self.kf = create_kalman_filter()

    def get_action(self, obs):
        """
        Computes the robot action based on current hand position received via socket.

        Args:
            obs (dict): Current environment observation containing the key 'robot0_eef_pos'.

        Returns:
            np.ndarray: Action array of shape (7,)
        """
        robot_eef_pos = obs['robot0_eef_pos']

        try:
            decoded_data = receive(self.s)

            palm_pos = np.mean(decoded_data, axis=0)

            if not self.calibrated:
                self.kf.x[:3] = palm_pos.reshape(3, 1)
                self.kf.x[3:] = 0
            else:
                self.kf.predict()
                self.kf.update(palm_pos)
                filtered_palm_pos = self.kf.x[:3].flatten()
                delta_hand_pos = self.hand_origin - filtered_palm_pos

            # Initialize the reference hand position after delay
            if not self.calibrated:
                if self.counter >= self.delay and np.all(np.abs(palm_pos) > 0):
                    self.hand_origin = palm_pos.copy()
                    self.calibrated = True
                self.counter += 1
                return np.zeros(7)

            # Compute delta pos in hand space and scale it to robot space
            delta_hand_pos = self.hand_origin - palm_pos
            delta_hand_pos = np.array([delta_hand_pos[2], delta_hand_pos[0], delta_hand_pos[1]]) # Z -> X, X -> Y, Y -> Z
            delta_hand_pos *= self.scale  # Apply scaling

            # Apply delta pos to the robot end effector
            target_pos = self.original_robot_pos + delta_hand_pos

            self.pid.reset(target=target_pos)
            delta = self.pid.update(robot_eef_pos, dt=self.dt)

            # Action: [dx, dy, dz, dqx, dqy, dqz, gripper]
            return np.array([delta[0], delta[1], delta[2], 0, 0, 0, getGripperState(decoded_data)])
        
        except Exception as e:
            print(f"[ERROR] During socket receive or processing: {e}")
            return np.zeros(7)  # Fallback action


# Helper Functions Used in the Lift Policy
def create_kalman_filter() -> object:
    """
    Helper to build kalman filter for smoothing hand tracking coordinates.
    
    Returns:
        Object: Kalman Filter Object
    
    """
    kf = KalmanFilter(dim_x=6, dim_z=3)

    dt = 0.01

    # State transition matrix (F)
    kf.F = np.array([
        [1, 0, 0, dt, 0,  0],
        [0, 1, 0, 0,  dt, 0],
        [0, 0, 1, 0,  0,  dt],
        [0, 0, 0, 1,  0,  0],
        [0, 0, 0, 0,  1,  0],
        [0, 0, 0, 0,  0,  1],
    ])

    # Measurement function (H)
    kf.H = np.array([
        [1, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
    ])

    # Covariance matrices
    kf.P *= 10.0   # Initial uncertainty
    kf.R *= 0.01   # Measurement noise
    kf.Q *= 0.001  # Process noise

    return kf

def getGripperState(landmarks: np.ndarray) -> int:
    """
        Returns state of gripper being open or closed given the eucliden / L2 distance of Index Finger and Thumb Landmarks

        Args:
            landmarks (np.ndarray): Hand Landmarks Array

        Returns:
            int: 1 when L2 distance from index to thumb is less than 0.1, -1 for all other cases
    """
    index_landmark = landmarks[8]
    thumb_landmark = landmarks[4]

    distance = np.linalg.norm(index_landmark-thumb_landmark)
    print(distance)
    if distance < 0.1: return 1
    
    return -1
