from enum import Enum

import numpy as np
import pygame

import gymnasium as gym
from gymnasium import spaces, register
from sympy.strategies.core import switch

from game.car import Car, MAX_SPEED
from game.engine import GameEngine
from game.track import Track
from settings import WINDOW_WIDTH, WINDOW_HEIGHT, FPS, RAY_LENGTH


class Actions(Enum):
    DO_NOTHING = 0
    ACCELERATE = 1
    BRAKE = 2
    TURN_LEFT = 3
    TURN_RIGHT = 4

class CarRacingEnv(gym.Env):
    metadata = {'render.render_modes': ["human"]}#, "rgb_array"]}

    def __init__(self, render_mode=None):
        super(CarRacingEnv, self).__init__()
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()

        self.engine = GameEngine(self.screen)
        # self.track = Track()
        # self.car = Car(*self.track.start_point)

        # Define action and observation space
        # Actions: [accelerate, brake, turn_left, turn_right]
        self.action_space = spaces.Discrete(4)

        # Observations: [speed, angle, ray_1 distance, ray_2, ray_3, ray_4, ray_5]
        self.observation_space = spaces.Box(
            low=np.array([-MAX_SPEED, -np.inf, 0, 0, 0, 0, 0 ]),
            high=np.array([MAX_SPEED, np.inf, RAY_LENGTH, RAY_LENGTH, RAY_LENGTH, RAY_LENGTH, RAY_LENGTH]),
            dtype=np.float32
        )

        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode


    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

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
        # TODO: Implement a better reward function
        if self.engine.car.dead:
            return -100
        return 1

    def render(self, mode='human'):
        self.engine.draw()

    def close(self):
        pygame.quit()

# register(
#     id='CarRacing-v0',
#     entry_point='gym.game_env:CarRacingEnv',
#     # max_episode_steps=1000,
#     # reward_threshold=900,
# )