from enum import Enum

import numpy as np
import pygame

import gymnasium as gym
from gymnasium import spaces

from game.car import MAX_SPEED, Car
from game.engine import GameEngine
from settings import WINDOW_WIDTH, WINDOW_HEIGHT, RAY_LENGTH, RAY_ANGLES


# class Actions(Enum):
#     DO_NOTHING = 0
#     ACCELERATE = 1
#     BRAKE = 2
#     TURN_LEFT = 3
#     TURN_RIGHT = 4


class Throttle(Enum):
    NO_ACTION = 0
    ACCELERATE = 1
    BRAKE = 2


class Steering(Enum):
    NO_ACTION = 0
    TURN_LEFT = 1
    TURN_RIGHT = 2


class CarRacingEnv(gym.Env):
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 60}

    def __init__(self, render_mode=None, no_fps_limiter=False, versus=False):
        super(CarRacingEnv, self).__init__()

        self.render_mode = render_mode
        self.no_fps_limiter = no_fps_limiter
        self.versus = versus

        assert (
            self.render_mode is None
            or self.render_mode in self.metadata["render_modes"]
        )

        pygame.init()
        if self.render_mode == "human":
            pygame.display.init()
            self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        else:  # mode == "rgb_array"
            self.screen = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))

        self.clock = pygame.time.Clock()
        self.engine = GameEngine(self.screen)
        if self.versus:
            self.player_car = Car(
                self.engine.track.start_point[0], self.engine.track.start_point[1]
            )  # Slight offset

        # Define action and observation space
        # # Actions: [do nothing, accelerate, brake, turn_left, turn_right]
        # self.action_space = spaces.Discrete(5)
        # Actions: [throttle, steering]
        # Throttle: 0 = no action, 1 = accelerate, 2 = brake
        # Steering: 0 = no action, 1 = turn left, 2 = turn right
        self.action_space = spaces.MultiDiscrete([3, 3])

        # Observations: [x, y, speed, angle, ray_1 distance, ray_2, ray_3, ..., ray_n]
        self.observation_space = spaces.Box(
            low=np.array([0, 0, -MAX_SPEED, -np.inf] + [0] * len(RAY_ANGLES)),
            high=np.array([1, 1, MAX_SPEED, np.inf] + [RAY_LENGTH] * len(RAY_ANGLES)),
            dtype=np.float64,
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
        # if action == Actions.ACCELERATE.value:
        #     self.engine.car.accelerate()
        # elif action == Actions.BRAKE.value:
        #     self.engine.car.brake()
        # elif action == Actions.TURN_LEFT.value:
        #     self.engine.car.turn_left()
        # elif action == Actions.TURN_RIGHT.value:
        #     self.engine.car.turn_right()
        throttle, steering = action  # Unpack actions
        if throttle == Throttle.ACCELERATE.value:
            self.engine.car.accelerate()
        elif throttle == Throttle.BRAKE.value:
            self.engine.car.brake()

        if steering == Steering.TURN_LEFT.value:
            self.engine.car.turn_left()
        elif steering == Steering.TURN_RIGHT.value:
            self.engine.car.turn_right()

        self.engine.car.update(self.engine.track)
        self.engine.car.check_collision(self.engine.track)
        self.engine.check_checkpoints()

        # If the distance per time spent is bad enough, the car is considered dead
        if (
            self.engine.elapsed_time > 10
            and (self.engine.car.distance_traveled / self.engine.elapsed_time) < 30
        ):
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
            (car.position.y - WINDOW_HEIGHT / 2) / WINDOW_HEIGHT,
        ]
        return np.array(
            normalized_positions + [car.speed / MAX_SPEED, car.angle] + normalized_rays,
            dtype=np.float32,
        )

    def _get_reward(self):
        reward = 0

        rewards_sources = {
            "collision_penalty": 0,
            "progress_reward": 0,
            "checkpoint_reward": 0,
            "speed_penalty": 0,
            "speed_bonus": 0,
            "total_reward": 0,
        }

        # Collision penalty
        if self.engine.car.dead:
            reward -= 50
            return reward

        # Progress reward
        reward += (
            self.engine.car.distance_traveled - self.last_distance_traveled
        ) * 0.2
        self.last_distance_traveled = self.engine.car.distance_traveled

        # Checkpoint reward
        if self.engine.current_checkpoint_index > self.last_checkpoint_index:
            reward += 75
            rewards_sources["checkpoint_reward"] = 75
            self.last_checkpoint_index = self.engine.current_checkpoint_index
            # print("Checkpoint reward: 100")

        # Speed penalty
        # if self.engine.car.speed < 0:
        #     reward -= 1
        if self.engine.car.speed > 0:
            reward += 0.5
        if self.engine.car.speed == 0:
            reward -= 2  # Réduire la pénalité si nécessaire
        elif self.engine.car.speed >= MAX_SPEED - 0.1:
            reward += 1

        # Récupérer les distances des rayons
        # rays = self.engine.car.rays_distances

        # Le rayon du milieu est celui à 0° (celui de la position centrale)
        # max_ray_index = rays.index(max(rays))
        # print(f"Rays: {max(rays).}")
        # print(f"Rays: {max(rays)}")

        # Vérifier si le rayon à 0° est le plus long
        # if max_ray_index != 2:  # Si le rayon du milieu est le plus long
        # print(f"Max ray index: {max_ray_index}")
        # reward -= 2 # Pénalité

        # reward += (self.engine.car.distance_traveled - self.last_distance_traveled) * 0.2

        # print(f"Reward: {reward}")

        # 5. Ray-based rewards
        rays = self.engine.car.rays_distances
        min_distance = min(rays)
        if min_distance < 25:
            reward -= 5

        # left_rays = sum(rays[:len(rays)//2])
        # right_rays = sum(rays[len(rays)//2 + 1:])
        # if abs(left_rays - right_rays) > 25:
        #     reward -= 5

        # if rays[0] > 100 or rays[-1] > 100:
        #     reward -= 5

        return reward

    def render(self, mode="human"):
        if self.versus:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                self.player_car.accelerate()
            if keys[pygame.K_DOWN]:
                self.player_car.brake()
            if keys[pygame.K_LEFT]:
                self.player_car.turn_left()
            if keys[pygame.K_RIGHT]:
                self.player_car.turn_right()

            if not self.player_car.dead:
                self.player_car.update(self.engine.track)
                self.player_car.check_collision(self.engine.track)
            self._draw_player_car()

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

    def _draw_player_car(self):
        # Draw a second car similarly to self.engine.car
        car_surface = pygame.Surface(
            (self.player_car.width, self.player_car.height), pygame.SRCALPHA
        )
        pygame.draw.rect(
            car_surface,
            (0, 255, 0),
            (0, 0, self.player_car.width, self.player_car.height),
        )
        rotated_image = pygame.transform.rotate(car_surface, -self.player_car.angle)
        rect = rotated_image.get_rect(center=self.player_car.position)
        self.screen.blit(rotated_image, rect.topleft)

    def close(self):
        pygame.quit()
