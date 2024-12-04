# main.py

import pygame
from game.car import Car
from game.engine import GameEngine
from game.track import Track
from settings import WINDOW_WIDTH, WINDOW_HEIGHT, FPS


def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    engine = GameEngine(screen)
    engine.run()

    pygame.quit()


if __name__ == "__main__":
    main()
