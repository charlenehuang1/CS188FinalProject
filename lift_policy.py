import numpy as np
import robosuite as suite
import socket
import pickle


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
        # data = self.s.recv(1024 * 100)
        # decoded_data = pickle.loads(data)
        # print(decoded_data)
        # # print(hand_landmarks)
        # return np.array([0, 0, 0, 0, 0, 0, 1])

        try:
            decoded_data = receive(self.s)
            print(decoded_data)
            return np.array([0, 0, 0, 0, 0, 0, 1])  # Placeholder action
        except Exception as e:
            print(f"Error during socket receive: {e}")
        return np.zeros(7)  # Safe fallback action
