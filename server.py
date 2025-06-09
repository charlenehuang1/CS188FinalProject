import socket
import pickle
import numpy as np
import struct

# Need to make these global since connect will only be called once but the connection will be broken when the robosuite task finishes
s = None
addr = None
c = None

def connect() -> None:
    """Initialize socket on localhost on port 3000 and wait for client connection"""
    global s
    global addr
    global c
    s = socket.socket()
    host = socket.gethostname()
    port = 3000
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
    s.listen(1)
    c, addr = s.accept()
    print(f'got connection from addr: {addr})')

def send(data):
    """
    Serialize and send Python object over socket to client
    
    Args:
        data (Any): The Python object to serialize and send.
    """

    try:
        data = pickle.dumps(data)
        length = struct.pack('>I', len(data))  # 4-byte length prefix
        c.sendall(length + data)
    except BrokenPipeError:
        print("Connection lost. Unable to send data.")
