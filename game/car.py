# car.py
from cgitb import small

import pygame
import math

from settings import CAR_WIDTH, CAR_HEIGHT, CAR_COLOR, RAY_LENGTH, RAY_ANGLES

MAX_SPEED = 2
ACCELERATION = 0.2
BRAKE_DECELERATION = 0.3
FREE_DECELERATION = 0.1
TURN_SPEED = 5


class Car:
    width = CAR_WIDTH
    height = CAR_HEIGHT
    color = CAR_COLOR

    angle = 0
    speed = 0

    dead = False

    def __init__(self, x, y):
        self.position = pygame.math.Vector2(x, y)
        self.last_position = self.position.copy()
        self.distance_traveled = 0
        self.rays_distances = [0] * len(RAY_ANGLES)

        # Créer l'image et le masque de la voiture
        self.original_image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(self.original_image, (255, 0, 0), (0, 0, self.width, self.height))
        self.image = self.original_image
        self.rect = self.image.get_rect(center=self.position)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, track):
        if self.dead:
            return

        self.last_position = self.position.copy()
        # Mise à jour de la position
        rad = math.radians(self.angle)
        self.position.x += math.cos(rad) * self.speed
        self.position.y += math.sin(rad) * self.speed

        # Calculate distance traveled in this step
        distance = math.sqrt(
            (self.position.x - self.last_position.x) ** 2 +
            (self.position.y - self.last_position.y) ** 2
        )
        self.distance_traveled += distance

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

        self.rays_distances = self.cast_rays(track)

    def draw(self, surface):
        # Draw the car as a rotated rectangle
        car_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(car_surface, self.color, (0, 0, self.width, self.height))
        rotated_image = pygame.transform.rotate(car_surface, -self.angle)
        rect = rotated_image.get_rect(center=self.position)
        surface.blit(rotated_image, rect.topleft)

    def draw_rays(self, surface):
        # Draw the rays
        distances = self.rays_distances
        for (start, end), distance in zip(self.get_rays(), distances):
            # Calculate the endpoint of the ray
            endpoint_x = start[0] + (end[0] - start[0]) * distance / RAY_LENGTH
            endpoint_y = start[1] + (end[1] - start[1]) * distance / RAY_LENGTH
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
        for ray_angle in RAY_ANGLES:
            total_angle = self.angle + ray_angle
            rad = math.radians(total_angle)
            end_x = self.position.x + math.cos(rad) * RAY_LENGTH
            end_y = self.position.y + math.sin(rad) * RAY_LENGTH
            rays.append(((self.position.x, self.position.y), (end_x, end_y)))
        return rays

    def cast_rays(self, track):
        """Cast rays and detect distances to track boundaries or when they leave the track."""
        distances = []
        for start, end in self.get_rays():
            ray_length = RAY_LENGTH
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
                    # print("Collision detected at corner:", corner)
                    self.speed = 0
                    self.dead = True
                    return True
            else:
                print("Corner out of bounds:", corner)
                self.speed = 0
                self.dead = True
                return True
        return False