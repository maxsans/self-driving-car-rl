import json
import os
import pygame
from settings import WINDOW_WIDTH, WINDOW_HEIGHT, BASE_DIR

TRACK_1 = "track_1.json"
TRACK_2 = "track_2.json"
TRACK_3 = "track_3.json"
TRACK_4 = "track_4.json"
TRACK_5 = "track_5.json"
TRACK_6 = "track_6.json"
class Track:
    def __init__(self, track_file=TRACK_4):
        self._load_track_data(track_file)
        self._load_image()
        self._load_metadata()
        self._load_mask()

    def _load_track_data(self, track_file):
        """Charge les données du fichier JSON."""
        track_path = os.path.join(BASE_DIR, "assets", track_file)
        if not os.path.exists(track_path):
            raise FileNotFoundError(f"Le fichier {track_path} n'existe pas.")

        with open(track_path, "r") as file:
            self._data = json.load(file)

        if "path" not in self._data or "checkpoints" not in self._data:
            raise ValueError("Le fichier JSON est mal structuré. 'path' et 'checkpoints' sont requis.")

    def _load_image(self):
        """Charge et redimensionne l'image de la piste."""
        image_path = os.path.join(BASE_DIR, "assets", self._data["path"])
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"L'image de la piste {image_path} est introuvable.")

        original_image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(original_image, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.rect = self.image.get_rect()

    def _load_mask(self):
        """Crée un masque pour détecter les bordures du circuit."""
        self._mask = pygame.mask.from_threshold(self.image, (255, 255, 255), (10, 10, 10))

    def _load_metadata(self):
        """Charge les métadonnées de la piste."""
        self.checkpoints = self._data.get("checkpoints", [])
        self.start_point = self._data.get("start_position", (0, 0))

    def draw(self, surface):
        """Dessine la piste."""
        surface.blit(self.image, (0, 0))

    def draw_checkpoints(self, surface):
        """Dessine les checkpoints comme des lignes."""
        for point1, point2 in self.checkpoints:
            pygame.draw.line(surface, (0, 0, 255), point1, point2, 5)