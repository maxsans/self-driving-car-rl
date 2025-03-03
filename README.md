# Car Racing Reinforcement Learning

This project implements a car racing game using reinforcement learning algorithms. The car's movement and collision detection are handled using Pygame, and the reinforcement learning models are trained using Stable Baselines3.

![Image 1](https://raw.githubusercontent.com/maxsans/self-driving-car-rl/main/assets/width_1600.webp)
![Image 2](https://raw.githubusercontent.com/maxsans/self-driving-car-rl/main/assets/image_demo.webp)
![Image 3](https://raw.githubusercontent.com/maxsans/self-driving-car-rl/main/assets/width_471.webp)


## Project Structure

- `game/`: Contains the game logic, car movement, raycasting methods, collision detection, etc.
- `rl/load.py`: Loads a pre-trained reinforcement learning model and runs it in the car racing environment.
- `rl/PPO.py`: Trains a PPO model on the car racing environment and evaluates its performance.

## Requirements

- Python 3.x
- Pygame
- Stable Baselines3

## Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/JAWS-tm/car-racing-rl.git
   cd car-racing-rl
   ```

2. Install the required packages:
   ```sh
   pip install -r requirements.txt
   ```

## Usage

### Training the Model

To train the PPO model, run:

```sh
python -m rl.PPO
```

### Start TensorBoard

To visualize the training progress, run:

```sh
tensorboard --logdir=./ppo_tensorboard/
```

### Models

All models are available in the folder `./all-models`, and all checkpoints for the models are stored in `./checkpoint-models`.

We conducted five training sessions:

1. **First Training**: This was a test with simple rewards, trained for 4,000,000 steps (~30 minutes).
2. **Second Training**: Used the same rewards as the first, but extended the training to 8,000,000 steps (~1 hour).
3. **Third Training**: Introduced new rewards to center the car on the track, with 18,000,000 steps (~2 hours).
4. **Fourth Training**: Maintained the updated rewards and extended the training to 22,000,000 steps (~3 hours).
5. **Fifth Training**: Used the same rewards as the previous sessions but trained for 75,000,000 steps (~10 hours). This model is the default model used in **rl/load.py**.

### Modes

`env = CarRacingEnv(render_mode="human", no_fps_limiter=False, versus=True)`

- `render_mode="human"`: Displays the game window.
- `render_mode="rgb_array"`: Runs without displaying the game window.
- `no_fps_limiter`: Removes the FPS limit (useful for running at the maximum FPS your computer can handle).
- **Versus Mode**: Allows you to play against the AI.

### Key Bindings

- Press **C** to toggle the display of checkpoints.
- Press **T** to toggle the display of rays.
- Press **R** to reset your car and the AI car.
