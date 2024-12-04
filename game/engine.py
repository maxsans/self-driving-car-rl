# engine.py

import pygame
from game.car import Car
from game.track import Track
from settings import *

class GameEngine:
    def __init__(self, screen):
        self.screen = screen
        # Initialize track and car
        self.track = Track()
        self.car = Car(*self.track.start_point)
        pygame.display.set_caption("Simulation de Conduite Autonome 2D")
        self.clock = pygame.time.Clock()

        self.running = True
        self.show_rays = True


    def reset(self):
        """Reset the game to its initial state."""
        self.car = Car(*self.track.start_point)
        self.running = True

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(FPS) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_t:
                        self.show_rays = not self.show_rays

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
            self.car.check_collision(self.track)


            if self.car.dead:
                print("Car crashed!")
                self.reset()
            # distances = self.car.cast_rays(self.track)

            # Render simulation
            self.screen.fill((0, 0, 0))
            self.track.draw(self.screen)
            self.car.draw(self.screen)
            if self.show_rays:
                self.car.draw_rays(self.screen, self.track)
            pygame.display.flip()

