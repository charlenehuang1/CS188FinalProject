import socket
import numpy
import pickle

s = socket.socket()
host = socket.gethostname()
port = 12345

s.connect((host, port))
data = s.recv(1024)
decoded_data = pickle.loads(data)
print(decoded_data)
s.close()
