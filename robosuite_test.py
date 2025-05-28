import robosuite as suite
import numpy as np
from lift_policy import LiftPolicy

# create environment instance
env = suite.make(
    env_name="Lift", 
    robots=["Panda"],  # try with other robots like "Sawyer" and "Jaco", start as "Panda"; also tested "IIWA"
    has_renderer=True,
    has_offscreen_renderer=False,
    use_camera_obs=False, # change to True maybe???? idk if we need
)

success_rate = 0
# reset the environment
for _ in range(5):
    obs = env.reset()
    print(obs)
    policy = LiftPolicy(obs) 
    while True:
        action = policy.get_action(obs)
        obs, reward, done, info = env.step(action)  # take action in the environment

        env.render()  # render on display
        if reward == 1.0:
            success_rate += 1
            break

success_rate /= 5.0
print('success rate:', success_rate)