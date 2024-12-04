# game/engine.py
import pygame
from settings import WHITE, SCREEN_WIDTH, SCREEN_HEIGHT
from game.car import Vehicle
from game.track import Environment

class GameEngine:
    def __init__(self, screen):
        self.screen = screen
        self.vehicle = Vehicle()
        self.environment = Environment()

    def update(self):
        # Mettre à jour les objets du jeu
        self.vehicle.update()
        self.environment.update()

    def render(self):
        # Dessiner le jeu
        self.screen.fill(WHITE)
        self.environment.render(self.screen)
        self.vehicle.render(self.screen)
