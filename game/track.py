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
            pygame.Rect(300, 70, 5, 60),
            pygame.Rect(350, 70, 5, 60),
            pygame.Rect(400, 70, 5, 60),
            pygame.Rect(445, 70, 5, 60),
            pygame.Rect(450, 130, 60, 5),
            pygame.Rect(450, 164, 60, 5),
            pygame.Rect(510, 169, 5, 60),
            pygame.Rect(550, 169, 5, 60),
            pygame.Rect(600, 169, 5, 60),
            pygame.Rect(656, 169, 5, 60),
            pygame.Rect(661, 229, 60, 5),
            pygame.Rect(661, 260, 60, 5),
            pygame.Rect(661, 310, 60, 5),
            pygame.Rect(661, 350, 60, 5),
            pygame.Rect(661, 397, 60, 5),
            pygame.Rect(656, 402, 5, 60),
            pygame.Rect(600, 402, 5, 60),
            pygame.Rect(550, 402, 5, 60),
            pygame.Rect(500, 402, 5, 60),
            pygame.Rect(450, 402, 5, 60),
            pygame.Rect(400, 402, 5, 60),
            pygame.Rect(348, 402, 5, 60),
            pygame.Rect(288, 462, 60, 5),
            pygame.Rect(288, 496, 60, 5),
            pygame.Rect(283, 501, 5, 60),
            pygame.Rect(230, 501, 5, 60),
            pygame.Rect(180, 501, 5, 60),
            pygame.Rect(132, 501, 5, 60),
            pygame.Rect(72, 496, 60, 5),
            pygame.Rect(72, 450, 60, 5),
            pygame.Rect(72, 400, 60, 5),
            pygame.Rect(72, 350, 60, 5),
            pygame.Rect(72, 300, 60, 5),
            pygame.Rect(72, 250, 60, 5),
            pygame.Rect(72, 210, 60, 5),
            pygame.Rect(72, 170, 60, 5),
            pygame.Rect(72, 130, 60, 5),
            pygame.Rect(132, 70, 5, 60),
            pygame.Rect(190, 70, 5, 60),
            pygame.Rect(250, 70, 5, 60)
        ]

    def draw(self, surface):
        # Dessiner l'image de la piste à la position (0, 0)
        surface.blit(self.image, (0, 0))

    def draw_checkpoints(self, surface):
        for checkpoint in self.checkpoints:
            pygame.draw.rect(surface, (0, 0, 128), checkpoint)

