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
TRACK_1_PATH = os.path.join(BASE_DIR, "assets", "track_1.json")
TRACK_2_PATH = os.path.join(BASE_DIR, "assets", "track_2.json")
TRACK_3_PATH = os.path.join(BASE_DIR, "assets", "track_3.json")
TRACK_4_PATH = os.path.join(BASE_DIR, "assets", "track_4.json")
TRACK_5_PATH = os.path.join(BASE_DIR, "assets", "track_5.json")
TRACK_6_PATH = os.path.join(BASE_DIR, "assets", "track_6.json")

# RL settings
RAY_LENGTH = 200
RAY_ANGLES = [-90, -60, -30, 0, 30, 60, 90]
