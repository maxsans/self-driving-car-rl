# settings.py
import os

# Window settings
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60

# Car settings
CAR_WIDTH = 25
CAR_HEIGHT = 15
CAR_COLOR = (255, 0, 0)

# Track settings
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TRACK_IMAGE_PATH = os.path.join(BASE_DIR, 'assets', 'track.png')

# RL settings
RAY_LENGTH = 200
RAY_ANGLES = [-30, 0, 30, 90, -90]

