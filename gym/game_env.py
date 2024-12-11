from enum import Enum

import numpy as np
import pygame

import gymnasium as gym
from gymnasium import spaces
from torch.backends.quantized import engine

from game.car import MAX_SPEED
from game.engine import GameEngine
from settings import WINDOW_WIDTH, WINDOW_HEIGHT, RAY_LENGTH


class Actions(Enum):
    DO_NOTHING = 0
    ACCELERATE = 1
    BRAKE = 2
    TURN_LEFT = 3
    TURN_RIGHT = 4

class CarRacingEnv(gym.Env):
    metadata = {'render_modes': ["human", "rgb_array"], 'render_fps': 30}

    def __init__(self, render_mode=None):
        super(CarRacingEnv, self).__init__()

        self.render_mode = render_mode

        assert self.render_mode is None or self.render_mode in self.metadata["render_modes"]

        pygame.init()
        if self.render_mode == "human":
            pygame.display.init()
            self.screen = pygame.display.set_mode(
                (WINDOW_WIDTH, WINDOW_HEIGHT)
            )
        else:  # mode == "rgb_array"
            self.screen = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))


        self.clock = pygame.time.Clock()

        self.engine = GameEngine(self.screen)

        # Define action and observation space
        # Actions: [accelerate, brake, turn_left, turn_right]
        self.action_space = spaces.Discrete(4)

        # Observations: [speed, angle, ray_1 distance, ray_2, ray_3, ray_4, ray_5]
        self.observation_space = spaces.Box(
            low=np.array([-MAX_SPEED, -np.inf, 0, 0, 0, 0, 0 ]),
            high=np.array([MAX_SPEED, np.inf, RAY_LENGTH, RAY_LENGTH, RAY_LENGTH, RAY_LENGTH, RAY_LENGTH]),
            dtype=np.float64
        )

        if self.render_mode == "human":
            self.render()


    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        print("RESET env")

        self.engine.reset()
        return self._get_obs(), {}

    def step(self, action):
        if action == Actions.ACCELERATE.value:
            self.engine.car.accelerate()
        elif action == Actions.BRAKE.value:
            self.engine.car.brake()
        elif action == Actions.TURN_LEFT.value:
            self.engine.car.turn_left()
        elif action == Actions.TURN_RIGHT.value:
            self.engine.car.turn_right()

        self.engine.car.update()
        self.engine.car.check_collision(self.engine.track)

        obs = self._get_obs()
        reward = self._get_reward()
        terminated = self.engine.car.dead
        truncated = False
        info = {}

        return obs, reward, terminated, truncated, info

    def _get_obs(self):
        ray_distances = self.engine.car.cast_rays(self.engine.track)
        return np.array([self.engine.car.speed, self.engine.car.angle] + ray_distances, dtype=np.float32)

    def _get_reward(self):
        reward = 0

        # Reward for moving forward
        if self.engine.car.speed > 0:
            reward += 5
        else:
            reward -= 10

        # Penalty for collisions
        if self.engine.car.dead:
            reward -= 100

        return reward

    def render(self, mode='human'):
        self.engine.draw()

        if self.render_mode == "human":
            pygame.event.pump()
            self.clock.tick(self.metadata["render_fps"])
            pygame.display.flip()

        elif self.render_mode == "rgb_array":
            return np.transpose(
                np.array(pygame.surfarray.pixels3d(self.screen)), axes=(1, 0, 2)
            )

        if self.clock is None:
            self.clock = pygame.time.Clock()

    def close(self):
        pygame.quit()

# register(
#     id='CarRacing-v0',
#     entry_point='gym.game_env:CarRacingEnv',
#     # max_episode_steps=1000,
#     # reward_threshold=900,
# )