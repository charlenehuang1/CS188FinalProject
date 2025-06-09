import struct
import socket
import numpy as np
import pickle

def recvall(sock: socket, n: int) -> bytes:
    """
    Helper to receive exactly n bytes from the socket

    Args:
        sock (socket): Socket for client
        n (int): Number of bytes to recieve

    Returns:
        bytes: byte stream of data recieved from the socket of length n
    """
    data = b''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            raise ConnectionError("Socket connection broken")
        data += packet
    return data

def receive(sock:socket) -> np.ndarray:
    """
    Receive a full pickle-encoded object sent with 4-byte length prefix

    Args:
        sock (socket): Socket for client

    Returns:
        np.ndarray: Hand Landmark Array 
    """
    raw_len = recvall(sock, 4)
    if not raw_len:
        raise ConnectionError("Failed to receive data length")
    msg_len = struct.unpack('>I', raw_len)[0]
    msg = recvall(sock, msg_len)
    return pickle.loads(msg)