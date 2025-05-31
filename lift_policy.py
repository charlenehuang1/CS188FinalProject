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


class LiftPolicy(object):
    """
    A simple PID-based policy for a robotic arm to lift an object in three phases:
    1. Move above the object.
    2. Lower to grasp the object.
    3. Lift the object.

    The policy uses a PID controller to drive the robot's end-effector to a sequence of target positions
    while managing the gripper state based on the current phase of motion.
    """

    def __init__(self, obs):
        """
        Initialize the LiftPolicy with the first observation from the environment.

        Args:
            obs (dict): Initial observation from the environment. Must include:
                - 'cube_pos': The position of the cube to be lifted.
        """
        self.s = socket.socket()
        self.host = socket.gethostname()
        self.port = 3000
        self.s.connect((self.host, self.port))
        self.original_robot_pos = obs['robot0_eef_pos']
        self.pid = PID(kp=10, ki=0, kd=0, target=obs['robot0_eef_pos']) 
        self.dt = 0.01

        self.delay = 5
        self.counter = 0
        
        self.original_hand_pose = np.array([None, None, None])
        
    def get_action(self, obs):
        """
        Compute the next action for the robot based on current observation.

        Args:
            obs (dict): Current observation. Must include:
                - 'robot0_eef_pos': Current end-effector position.
                - 'cube_pos': Current position of the cube.

        Returns:
            np.ndarray: 7D action array for robosuite OSC:
                - action[-1]: Gripper command (1 to close, -1 to open)
        """
        robot_eef_pos = obs['robot0_eef_pos']
        try:
            decoded_data = receive(self.s)
            wrist_pos = decoded_data[0]

            if not self.original_hand_pose[0]:
                if wrist_pos[0] != 0 and self.counter >= self.delay: self.original_hand_pose = wrist_pos
                self.counter += 1
            delta_hand_pos = self.original_hand_pose - wrist_pos
            delta_hand_pos = np.array([delta_hand_pos[0], delta_hand_pos[1], 0])
            print(f'DELTA HAND: {delta_hand_pos}, ORIGINAL ROBOT: {self.original_robot_pos}')
            target_pos = self.original_robot_pos - delta_hand_pos
            print(f'EEF: {robot_eef_pos}, TARGET: {target_pos}')
            self.pid.reset(target=target_pos)
            delta = self.pid.update(robot_eef_pos, dt=self.dt)
            # print(f'TARGET: {target_pos}, EEF: {robot_eef_pos}, DELTA: {delta}')
            return np.array([delta[2], delta[1], 0, 0, 0, 0, 1])  # Placeholder action
        except Exception as e:
            print(f"Error during socket receive: {e}")
        return np.zeros(7)  # Safe fallback action
