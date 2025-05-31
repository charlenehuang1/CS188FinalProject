import numpy as np
import robosuite as suite
import socket
import pickle
from pid import PID


import struct

def recvall(sock, n):
    """Helper to receive exactly n bytes from the socket"""
    data = b''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            raise ConnectionError("Socket connection broken")
        data += packet
    return data

def receive(sock):
    """Receive a full pickle-encoded object sent with 4-byte length prefix"""
    raw_len = recvall(sock, 4)
    if not raw_len:
        raise ConnectionError("Failed to receive data length")
    msg_len = struct.unpack('>I', raw_len)[0]
    msg = recvall(sock, msg_len)
    return pickle.loads(msg)

def getGripperState(landmarks):
    index_landmark = landmarks[8]
    thumb_landmark = landmarks[4]

    distance = np.linalg.norm(index_landmark)
    print(distance)
    if distance > 0.7: return 1
    
    return -1


class LiftPolicy(object):
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

        self.scale = np.array([4.0, 1, 2])  # Scaling factor between hand movement and robot motion

    def get_action(self, obs):
        robot_eef_pos = obs['robot0_eef_pos']

        try:
            decoded_data = receive(self.s)
            wrist_pos = np.array(decoded_data[0], dtype=np.float32)  # [x, y, z] in MediaPipe space

            palm_pos = np.mean(decoded_data, axis=0)

            # Initialize the reference hand position after a short delay
            if not self.calibrated:
                if self.counter >= self.delay and np.all(np.abs(wrist_pos) > 0):
                    self.hand_origin = palm_pos.copy()
                    self.calibrated = True
                    print(f"Calibrated hand origin at: {self.hand_origin}")
                self.counter += 1
                return np.zeros(7)  # Wait until calibrated

            # Compute delta in hand space and scale it to robot space
            delta_hand_pos = self.hand_origin - palm_pos
            #delta_hand_pos = np.array([delta_hand_pos[1], -delta_hand_pos[0], -delta_hand_pos[2]])  # Flatten Z for now
            delta_hand_pos = np.array([
                delta_hand_pos[2],     # Forward/backward
                delta_hand_pos[0],    # Left/right
                delta_hand_pos[1],    # Up/down
            ])
            delta_hand_pos *= self.scale  # Apply scaling

            target_pos = self.original_robot_pos + delta_hand_pos

            self.pid.reset(target=target_pos)
            delta = self.pid.update(robot_eef_pos, dt=self.dt)

            # Action: [dx, dy, dz, dqx, dqy, dqz, gripper]
            return np.array([delta[0], delta[1], delta[2], 0, 0, 0, getGripperState(decoded_data)])
        
        except Exception as e:
            print(f"[ERROR] During socket receive or processing: {e}")
            return np.zeros(7)  # Fallback safe action
