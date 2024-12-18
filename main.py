# main.py

import pygame

from envs.game_env import CarRacingEnv, Throttle, Steering


def main():
    env = CarRacingEnv(render_mode="human")
    obs = env.reset()
    terminated = False

    while not terminated:
        # action = env.action_space.sample()  # Replace with your action selection logic

        throttle = Throttle.NO_ACTION.value
        steering = Steering.NO_ACTION.value
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            throttle = Throttle.ACCELERATE.value
        elif keys[pygame.K_DOWN]:
            throttle = Throttle.BRAKE.value
        if keys[pygame.K_LEFT]:
            steering = Steering.TURN_LEFT.value
        elif keys[pygame.K_RIGHT]:
            steering = Steering.TURN_RIGHT.value

        obs, reward, terminated, truncated, info = env.step((throttle, steering))

    print("Done")

    env.close()

if __name__ == "__main__":
    main()



#
# def main():
#     pygame.init()
#     screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
#
#     engine = GameEngine(screen)
#     engine.run()
#
#     pygame.quit()
#

if __name__ == "__main__":
    main()
