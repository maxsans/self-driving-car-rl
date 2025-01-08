# engine.py

import pygame
from game.car import Car
from game.track import Track
from settings import *
import matplotlib.pyplot as plt
import random

class Checkbox:
    def __init__(self, x, y, width, height, text, initial=False):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (0, 0, 0)  # Set color to black
        self.checked = initial
        self.text = text
        self.font = pygame.font.Font(None, 24)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, 2)  # Draw box in black
        if self.checked:
            pygame.draw.line(surface, self.color, self.rect.topleft, self.rect.bottomright, 2)  # Draw cross in black
            pygame.draw.line(surface, self.color, self.rect.topright, self.rect.bottomleft, 2)  # Draw cross in black
        text_surf = self.font.render(self.text, True, self.color)  # Render text in black
        surface.blit(text_surf, (self.rect.x + self.rect.width + 10, self.rect.y))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.checked = not self.checked
                return self.checked
        return None

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

        self.font = pygame.font.Font(None, 36)
        self.start_time = pygame.time.get_ticks()
        self.pause_start_time = 0
        self.total_pause_time = 0
        self.paused = False
        self.car_positions = [[]] 
        self.colors = [(255, 0, 0)] 
        self.lap_count = 0
        self.lap_start_time = pygame.time.get_ticks()
        self.last_lap_time = 0
        self.elapsed_time = 0
        self.remaining_checkpoints = self.track.checkpoints.copy()
        self.current_checkpoint_index = 0
        self.show_checkpoints = True  # State for displaying checkpoints

        # Initialize checkbox
        self.checkbox = Checkbox(10, WINDOW_HEIGHT - 30, 20, 20, "Afficher les checkpoints", initial=True)

    def reset(self):
        """Reset the game to its initial state."""
        self.car = Car(*self.track.start_point)
        self.running = True

        self.car_positions.append([])
        self.colors.append((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        self.remaining_checkpoints = self.track.checkpoints.copy()
        self.current_checkpoint_index = 0
        self.lap_start_time = pygame.time.get_ticks()
        self.total_pause_time = 0
        self.start_time = pygame.time.get_ticks()
        self.elapsed_time = 0

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(FPS) / 1000

            self.handle_events()
            
            if not self.paused:
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
                self.car.update(self.track)
                self.car.check_collision(self.track)
                
                self.car_positions[-1].append((self.car.position.x, self.car.position.y))

                self.check_checkpoints()

                if self.current_checkpoint_index >= len(self.track.checkpoints):
                    self.lap_count += 1
                    self.last_lap_time = (pygame.time.get_ticks() - self.lap_start_time - self.total_pause_time) / 1000
                    print(f"Tour {self.lap_count} en {self.last_lap_time:.2f} secondes")
                    self.lap_start_time = pygame.time.get_ticks()
                    self.current_checkpoint_index = 0

            if self.car.dead:
                print("Car crashed!")
                self.total_pause_time = self.total_pause_time + (pygame.time.get_ticks() - self.start_time - self.total_pause_time)
                self.reset()

            self.draw()
            pygame.display.flip()

        # Save car path
        self.save_car_path(self.track.image, self.car_positions, self.colors)

    def draw(self):
        # Render simulation
        self.screen.fill((0, 0, 0))
        self.track.draw(self.screen)
        self.car.draw(self.screen)

        if self.show_rays:
            self.car.draw_rays(self.screen)

        self.elapsed_time = (pygame.time.get_ticks() - self.start_time - self.total_pause_time) / 1000
        timer_text = self.font.render(f"{self.elapsed_time:.2f}s", True, (0, 0, 0))
        if self.show_checkpoints:
            self.track.draw_checkpoints(self.screen)
        self.checkbox.draw(self.screen)
        self.screen.blit(timer_text, (WINDOW_WIDTH - timer_text.get_width() - 10, 10))

        # Display lap information
        lap_info = self.font.render(f"Tour {self.lap_count} en {self.last_lap_time:.2f}s", True, (0, 0, 0))
        self.screen.blit(lap_info, (10, 10))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.paused = not self.paused 
                if self.paused:
                    self.pause_start_time = pygame.time.get_ticks()
                else:
                    self.total_pause_time += pygame.time.get_ticks() - self.pause_start_time
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_t:
                    self.show_rays = not self.show_rays
            # Handle checkbox events
            new_state = self.checkbox.handle_event(event)
            if new_state is not None:
                self.show_checkpoints = new_state

    def save_car_path(self, track_image, car_positions, colors):
        track_array = pygame.surfarray.array3d(track_image)
        track_array = track_array.transpose([1, 0, 2])

        fig, ax = plt.subplots()
        ax.imshow(track_array)

        for positions, color in zip(car_positions, colors):
            if positions: 
                x_positions, y_positions = zip(*positions)
                ax.plot(x_positions, y_positions, color=[c/255 for c in color], linewidth=2)

    
        plt.savefig('car_path.png')
        plt.close()

    def check_checkpoints(self):
        if self.current_checkpoint_index < len(self.track.checkpoints):
            checkpoint = self.track.checkpoints[self.current_checkpoint_index]
            if self.car.rect.colliderect(checkpoint):
                self.current_checkpoint_index += 1

    def draw_checkpoints(self, surface):
        """Draw checkpoints if enabled."""
        for checkpoint in self.track.checkpoints:
            pygame.draw.rect(surface, (0, 0, 128), checkpoint)