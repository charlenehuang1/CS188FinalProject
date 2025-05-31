import socket
import pickle
import numpy as np

s = socket.socket()
host = socket.gethostname()
port = 12345

s.bind((host, port))

s.listen(1)

test_data = np.random.rand(2, 3)

while True:
    c, addr = s.accept()
    print(f'got connection from addr: {addr})')
    data = pickle.dumps(test_data)


    c.send(data)
    c.close()
