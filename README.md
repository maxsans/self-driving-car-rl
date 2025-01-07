# # Car Racing Reinforcement Learning

This project implements a car racing game using reinforcement learning algorithms. The car's movement and collision detection are handled using Pygame, and the reinforcement learning models are trained using Stable Baselines3.

## Project Structure

- `game/car.py`: Contains the car's movement logic, raycasting methods, and collision detection.
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
