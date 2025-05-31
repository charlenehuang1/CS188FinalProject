import socket
import numpy as np
import pickle
import robosuite as suite

s = socket.socket()
host = socket.gethostname()
port = 3000
s.connect((host, port))

env = suite.make(
    env_name="Lift", 
    robots=["Panda"],  # try with other robots like "Sawyer" and "Jaco", start as "Panda"; also tested "IIWA"
    has_renderer=True,
    has_offscreen_renderer=False,
    use_camera_obs=False, # change to True maybe???? idk if we need
)

env.render()

while True:
    data = s.recv(1024 * 10)
    decoded_data = pickle.loads(data)
    print(decoded_data)
