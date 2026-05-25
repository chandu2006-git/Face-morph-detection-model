import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "model", "FINAL_RENDER_SAFE.h5")

MODEL_URL = "https://drive.google.com/uc?id=1Uz3G-yS0fw6ik8HmuPura6VnVB4GYTRY"

IMAGE_SIZE = (299, 299)
THRESHOLD = 0.5