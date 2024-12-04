# car.py
from cgitb import small

import pygame
import math

MAX_SPEED = 2
ACCELERATION = 0.2
BRAKE_DECELERATION = 0.3
FREE_DECELERATION = 0.1
TURN_SPEED = 3
CAR_WIDTH = 25
CAR_HEIGHT = 15

class Car:
    def __init__(self, x, y):
        self.position = pygame.math.Vector2(x, y)
        self.angle = 0  # En degrés
        self.speed = 0

        self.width = CAR_WIDTH
        self.height = CAR_HEIGHT
        self.color = (255, 0, 0)


        # Créer l'image et le masque de la voiture
        self.original_image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(self.original_image, (255, 0, 0), (0, 0, self.width, self.height))
        self.image = self.original_image
        self.rect = self.image.get_rect(center=self.position)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        # Mise à jour de la position
        rad = math.radians(self.angle)
        self.position.x += math.cos(rad) * self.speed
        self.position.y += math.sin(rad) * self.speed

        # Appliquer la décélération libre
        if self.speed > 0:
            self.speed -= FREE_DECELERATION
        elif self.speed < 0:
            self.speed += FREE_DECELERATION

        # Éviter les petites valeurs flottantes
        if abs(self.speed) < FREE_DECELERATION:
            self.speed = 0

        # Mettre à jour le rectangle et le masque
        self.rect = self.image.get_rect(center=self.position)
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, surface):
        # Draw the car as a rotated rectangle
        car_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(car_surface, self.color, (0, 0, self.width, self.height))
        rotated_image = pygame.transform.rotate(car_surface, -self.angle)
        rect = rotated_image.get_rect(center=self.position)
        surface.blit(rotated_image, rect.topleft)
    ######################
    # Car Movement Logic #
    ######################
    def accelerate(self):
        if self.speed < MAX_SPEED:
            self.speed += ACCELERATION

    def brake(self):
        if self.speed > -MAX_SPEED / 2:
            self.speed -= BRAKE_DECELERATION

    def turn_left(self):
        if self.speed != 0:
            self.angle -= TURN_SPEED * (self.speed / MAX_SPEED)

    def turn_right(self):
        if self.speed != 0:
            self.angle += TURN_SPEED * (self.speed / MAX_SPEED)

    #############################
    # Collision Detection Logic #
    #############################
    def get_corners(self):
        """Calculate the four corners of the car after rotation."""
        half_width = self.width / 2
        half_height = self.height / 2

        # Calculate the offsets for each corner
        corners = [
            pygame.math.Vector2(-half_width, -half_height),  # Top-left
            pygame.math.Vector2(half_width, -half_height),   # Top-right
            pygame.math.Vector2(half_width, half_height),    # Bottom-right
            pygame.math.Vector2(-half_width, half_height),   # Bottom-left
        ]

        # Rotate corners and adjust to the car's position
        rotated_corners = [
            self.position + corner.rotate(self.angle) for corner in corners
        ]
        return rotated_corners

    def check_collision(self, track):
        """Check if any corner of the car is off the track."""
        corners = self.get_corners()
        for corner in corners:
            x, y = int(corner.x), int(corner.y)
            # Check if the corner is outside the track boundaries
            if 0 <= x < track.rect.width and 0 <= y < track.rect.height:
                color = track.image.get_at((x, y))
                if color == (255, 255, 255):
                    print("Collision detected at corner:", corner)
                    self.speed = 0
                    return True
            else:
                print("Corner out of bounds:", corner)
                self.speed = 0
                return True
        return False