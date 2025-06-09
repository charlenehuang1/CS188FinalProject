# CS 188 Final Project: Hand Tracking for Pick-Up Tasks in Robosuite

### ✍️ Authors

- [Charlene Huang](https://github.com/charlenehuang1)
- [Alexis Lee](https://github.com/alexissleee)
- [Daniel Chvat](https://github.com/DanielChvat)

Our project aims to apply hand tracking to the robot teleoperation task by translating physical hand positions to a simulated Panda robot arm in Robosuite. This project was primarily tested on the lift task in robosuite but due to the nature of teleoperation other tasks could be successfully completed without additional adaptation. 

### ⚡️ Requirements
> [!NOTE]  
>Mileage may vary with different package versions. We highly recommended **venv** or **conda** virtual environments. The packages listed below are the versions we used and are not representative of all verions that may work. 

| Package    | Version   |
|------------|-----------|
| Python     | 3.10.13   |
| Mediapipe  | 0.10.21   |
| Robosuite  | 1.5.1     |
| Mujoco     | 3.3.0     |
| OpenCV     | 4.11.0.86 |
| Numpy      | 1.26.4    |
| FilterPy   | 1.4.5     |

### 🚀 Running Project
- **Create a new conda environment**
```shell
$ conda create -n teleoperate python=3.10.13
```
- **Activate environment**
```shell
$ conda activate teleoperate
```

- **Clone the Repository**
```shell
$ git clone https://github.com/charlenehuang1/CS188FinalProject.git
$ cd CS188FinalProject
```

- **Install Required Packages**
```shell
$ pip install -r requirements.txt
```

- **Begin Hand Tracking**
```shell
$ python handtracking.py
```

> [!WARNING]   
> In order for the socket connection to be established correctly you must wait for the handtracking script to fully initialize opencv and mediapipe. This can be seen by the message **INFO: Created TensorFlow Lite XNNPACK delegate for CPU.** or something similar appearing in the console.

- **Begin Robosuite Simulation**

On **Windows** and **Linux**, run:
```shell
$ python robosuite_test.py
```
On **macOS**, due to Mujoco requirements, run:
```shell
$ mjpython robosuite_test.py
```



> [!WARNING]   
> The initial position of your hand when this script initalizes is used as a reference to compute displacement from the original position so we highly recommend to place your hand somewhere close to the middle of the camera view as possible to allow for as much movement in x, y, z as possible

### Project Demo
<video width="640" height="360" controls>
  <source src="https://github.com/charlenehuang1/CS188FinalProject/raw/main/CS%20188%20Demo%20Video.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

### 🔗 Links
- [🌐 Project Website](https://charlenehuang1.github.io/CS188FinalProjectWebsite/)
- [🛠️ Project Website Source](https://github.com/charlenehuang1/CS188FinalProjectWebsite)
- [🎬 Watch Our Demo Video](https://drive.google.com/file/d/1G6AGPgdSopS0yZ15LrFnfSstq9DNXww8/view?usp=sharing)
