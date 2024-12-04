# engine.py

import pygame
from game.car import Car
from game.track import Track
from settings import *

class Engine:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Autonomous Driving Simulation")
        self.clock = pygame.time.Clock()

        # Initialize simulation components
        self.track = Track()
        self.car = Car(150, 150)

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(FPS) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Input handling
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                self.car.accelerate()
            if keys[pygame.K_DOWN]:
                self.car.brake()
            if keys[pygame.K_LEFT]:
                self.car.turn_left()
            if keys[pygame.K_RIGHT]:
                self.car.turn_right()

            # Update simulation
            self.car.update()
            # distances = self.car.cast_rays(self.track)

            # Render simulation
            self.screen.fill((0, 0, 0))
            self.track.draw(self.screen)
            self.car.draw(self.screen)
            self.car.draw_rays(self.screen, self.track)
            pygame.display.flip()

        pygame.quit()
