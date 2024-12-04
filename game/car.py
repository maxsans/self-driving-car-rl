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

        # Raycasting
        self.ray_length = 200  # Max distance a ray can detect
        self.ray_angles = [-30, 0, 30, 90, -90]

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

    def draw_rays(self, surface, track):
        # Draw the rays
        distances = self.cast_rays(track)  # Get the distances for visualization
        for (start, end), distance in zip(self.get_rays(), distances):
            # Calculate the endpoint of the ray
            endpoint_x = start[0] + (end[0] - start[0]) * distance / self.ray_length
            endpoint_y = start[1] + (end[1] - start[1]) * distance / self.ray_length
            endpoint = (endpoint_x, endpoint_y)

            # Draw the ray
            pygame.draw.line(surface, (0, 255, 0), start, endpoint, 2)

            # Draw the ray's endpoint
            pygame.draw.circle(surface, (255, 0, 0), (int(endpoint_x), int(endpoint_y)), 3)

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

    ######################
    # Raycasting Methods #
    ######################
    def get_rays(self):
        """Calculate the end points of all rays relative to the car."""
        rays = []
        for ray_angle in self.ray_angles:
            total_angle = self.angle + ray_angle
            rad = math.radians(total_angle)
            end_x = self.position.x + math.cos(rad) * self.ray_length
            end_y = self.position.y + math.sin(rad) * self.ray_length
            rays.append(((self.position.x, self.position.y), (end_x, end_y)))
        return rays

    def cast_rays(self, track):
        """Cast rays and detect distances to track boundaries or when they leave the track."""
        distances = []
        for start, end in self.get_rays():
            ray_length = self.ray_length
            step = 1  # Ray increment in pixels
            for i in range(0, ray_length, step):
                x = int(start[0] + (end[0] - start[0]) * i / ray_length)
                y = int(start[1] + (end[1] - start[1]) * i / ray_length)

                # Check if the ray goes out of the track bounds
                if not (0 <= x < track.rect.width and 0 <= y < track.rect.height):
                    distances.append(i)  # Stop the ray when it goes out of bounds
                    break

                # Check the color of the pixel
                color = track.image.get_at((x, y))
                if color == (255, 255, 255):
                    distances.append(i)  # Distance to the boundary
                    break
            else:
                distances.append(ray_length)  # Max distance if no boundary or out of bounds
        return distances


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