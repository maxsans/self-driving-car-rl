# track.py

import pygame
from settings import WINDOW_WIDTH, WINDOW_HEIGHT

class Track:
    def __init__(self, image_path):
        self.original_image = pygame.image.load(image_path).convert()
        self.image = pygame.transform.scale(self.original_image, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.rect = self.image.get_rect()
        self.start_point = (150, 150)
        self.finish_point = (650, 450)

        # Créer un masque pour les bordures du circuit (pixels blancs)
        self.mask = pygame.mask.from_threshold(self.image, (255, 255, 255), (10, 10, 10))

    def draw(self, surface):
        # Dessiner l'image de la piste à la position (0, 0)
        surface.blit(self.image, (0, 0))
