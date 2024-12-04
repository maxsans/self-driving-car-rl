# car.py
from cgitb import small

import pygame
import math

class Car:
    def __init__(self, x, y, width=40, height=20):
        self.position = pygame.math.Vector2(x, y)
        self.angle = 0  # En degrés
        self.speed = 0
        self.max_speed = 3
        self.acceleration = 0.2
        self.brake_deceleration = 0.5
        self.free_deceleration = 0.1
        self.turn_speed = 5  # Degrés par frame
        self.width = width
        self.height = height
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
            self.speed -= self.free_deceleration
        elif self.speed < 0:
            self.speed += self.free_deceleration

        # Éviter les petites valeurs flottantes
        if abs(self.speed) < self.free_deceleration:
            self.speed = 0

        # Mettre à jour le rectangle et le masque
        self.rect = self.image.get_rect(center=self.position)
        self.mask = pygame.mask.from_surface(self.image)

    def accelerate(self):
        if self.speed < self.max_speed:
            self.speed += self.acceleration

    def brake(self):
        if self.speed > -self.max_speed / 2:
            self.speed -= self.brake_deceleration

    def turn_left(self):
        if self.speed != 0:
            self.angle -= self.turn_speed * (self.speed / self.max_speed)

    def turn_right(self):
        if self.speed != 0:
            self.angle += self.turn_speed * (self.speed / self.max_speed)

    def draw(self, surface):
        # Dessiner la voiture comme un rectangle
        car_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(car_surface, self.color, (0, 0, self.width, self.height))
        rotated_image = pygame.transform.rotate(car_surface, -self.angle)
        rotated_rect = rotated_image.get_rect(center=self.position)

        # Mettre à jour le masque pour la détection des collisions
        self.mask = pygame.mask.from_surface(rotated_image)

        surface.blit(rotated_image, rotated_rect.topleft)

    def check_collision(self, track):
        # Calculer le décalage entre la voiture et le circuit
        offset = (int(self.rect.left - track.rect.left), int(self.rect.top - track.rect.top))
        # Vérifier la collision entre les masques
        collision_point = track.mask.overlap(self.mask, offset)
        if collision_point:
            print("Collision détectée avec la bordure !")
            self.speed = 0