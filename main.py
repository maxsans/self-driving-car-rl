# main.py

import pygame
from game.car import Car
from game.engine import GameEngine
from game.track import Track
from settings import WINDOW_WIDTH, WINDOW_HEIGHT, FPS
from gym.game_env import CarRacingEnv
import gymnasium
from stable_baselines3.common.env_checker import check_env




def main():
    env = CarRacingEnv(render_mode="rgb_array")
    # obs = env.reset()
    terminated = False

    while not terminated:
        action = env.action_space.sample()  # Replace with your action selection logic
        obs, reward, terminated, truncated, info = env.step(action)
        env.render()

    print("Done")

    env.close()

if __name__ == "__main__":
    main()




# def main():
    # pygame.init()
    # screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    #
    # engine = GameEngine(screen)
    # engine.run()
    #
    # pygame.quit()

#
# if __name__ == "__main__":
#     main()
