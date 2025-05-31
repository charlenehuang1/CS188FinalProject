import socket
import pickle
import numpy as np
s = None
addr = None
c = None

import struct

def connect():
    global s
    global addr
    global c
    s = socket.socket()
    host = socket.gethostname()
    port = 3000
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
    s.listen(4)
    c, addr = s.accept()
    print(f'got connection from addr: {addr})')

def send(data):
    # data = pickle.dumps(data)
    # c.send(data)
    # # c.close()
    # # pass
    try:
        data = pickle.dumps(data)
        length = struct.pack('>I', len(data))  # 4-byte length prefix
        c.sendall(length + data)
    except BrokenPipeError:
        print("Connection lost. Unable to send data.")
