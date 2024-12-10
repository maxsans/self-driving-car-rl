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

        # Define checkpoints as rectangles (lines of height 60 pixels)
        self.checkpoints = [
            pygame.Rect(510, 169, 5, 60),
            pygame.Rect(656, 402, 5, 60),
            pygame.Rect(132, 501, 5, 60),
            pygame.Rect(250, 70, 5, 60)
        ]

    def draw(self, surface):
        # Dessiner l'image de la piste à la position (0, 0)
        surface.blit(self.image, (0, 0))

        # Draw checkpoints
        # for checkpoint in self.checkpoints:
        #     pygame.draw.rect(surface, (0, 255, 0), checkpoint)

