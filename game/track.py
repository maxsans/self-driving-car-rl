# track.py

import pygame
from settings import WINDOW_WIDTH, WINDOW_HEIGHT, TRACK_IMAGE_PATH


class Track:
    def __init__(self):
        self.original_image = pygame.image.load(TRACK_IMAGE_PATH).convert()
        self.image = pygame.transform.scale(self.original_image, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.rect = self.image.get_rect()
        self.start_point = (250, 100)

        # Créer un masque pour les bordures du circuit (pixels blancs)
        self.mask = pygame.mask.from_threshold(self.image, (255, 255, 255), (10, 10, 10))

    def draw(self, surface):
        # Dessiner l'image de la piste à la position (0, 0)
        surface.blit(self.image, (0, 0))

