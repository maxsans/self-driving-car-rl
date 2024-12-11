from enum import Enum

import numpy as np
import pygame

import gymnasium as gym
from gymnasium import spaces
from six import print_
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

    def __init__(self, render_mode=None, no_fps_limiter=False):
        super(CarRacingEnv, self).__init__()

        self.render_mode = render_mode
        self.no_fps_limiter = no_fps_limiter

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
        # Actions: [do nothing, accelerate, brake, turn_left, turn_right]
        self.action_space = spaces.Discrete(5)

        # Observations: [x, y, speed, angle, ray_1 distance, ray_2, ray_3, ray_4, ray_5]
        self.observation_space = spaces.Box(
            low=np.array([0, 0, -MAX_SPEED, -np.inf, 0, 0, 0, 0, 0 ]),
            high=np.array([1, 1, MAX_SPEED, np.inf, RAY_LENGTH, RAY_LENGTH, RAY_LENGTH, RAY_LENGTH, RAY_LENGTH]),
            dtype=np.float64
        )

        if self.render_mode == "human":
            self.render()

        self.last_distance_traveled = 0
        self.last_checkpoint_index = 0


    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        self.engine.reset()
        self.last_distance_traveled = 0
        self.last_checkpoint_index = 0
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

        self.engine.car.update(self.engine.track)
        self.engine.car.check_collision(self.engine.track)
        self.engine.check_checkpoints()

        # If the distance per time spent is bad enough, the car is considered dead
        if self.engine.elapsed_time > 10 and (self.engine.car.distance_traveled / self.engine.elapsed_time) < 30:
            self.engine.car.dead = True

        obs = self._get_obs()
        reward = self._get_reward()
        terminated = self.engine.car.dead
        info = {}

        if self.render_mode == "human":
            self.render()

        return obs, reward, terminated, False, info

    def _get_obs(self):
        car = self.engine.car
        ray_distances = car.rays_distances
        normalized_rays = [distance / RAY_LENGTH for distance in ray_distances]
        normalized_positions = [
            (car.position.x - WINDOW_WIDTH / 2) / WINDOW_WIDTH,
            (car.position.y - WINDOW_HEIGHT / 2) / WINDOW_HEIGHT
        ]
        return np.array(normalized_positions + [car.speed / MAX_SPEED, car.angle] + normalized_rays, dtype=np.float32)

    def _get_reward(self):
        reward = 0

        # Collision penalty
        if self.engine.car.dead:
            reward -= 500
            return reward


        # Progress reward
        reward += (self.engine.car.distance_traveled - self.last_distance_traveled) * 0.3
        self.last_distance_traveled = self.engine.car.distance_traveled

        # Checkpoint reward
        if self.engine.current_checkpoint_index > self.last_checkpoint_index:
            reward += 100
            self.last_checkpoint_index = self.engine.current_checkpoint_index
            # print("Checkpoint reward: 100")

        # Speed penalty
        if self.engine.car.speed <= 0:
            reward -= 10
        elif self.engine.car.speed >= MAX_SPEED - 0.1:
            reward += 1

        # if self.engine.car.speed > 0:
        #     # Encourage going fast (reward is exponential to speed [0, 8])
        #     reward += (self.engine.car.speed / MAX_SPEED) ** 2 * 4
        # else:
        #     # If not moving forward, penalize
        #     reward -= 10

        # 5. Ray-based rewards
        rays = self.engine.car.rays_distances
        min_distance = min(rays)
        if min_distance < 15:
            reward -= 10

        left_rays = sum(rays[:len(rays)//2])
        right_rays = sum(rays[len(rays)//2 + 1:])
        # reward -= abs(left_rays - right_rays) * 0.05
        if abs(left_rays - right_rays) > 30:
            reward -= 5

        return reward

    def render(self, mode='human'):
        self.engine.draw()

        if self.render_mode == "human":
            pygame.event.pump()
            if not self.no_fps_limiter:
                self.clock.tick(self.metadata["render_fps"])
            pygame.display.flip()

        elif self.render_mode == "rgb_array":
            return np.transpose(
                np.array(pygame.surfarray.pixels3d(self.screen)), axes=(1, 0, 2)
            )

    def close(self):
        pygame.quit()
