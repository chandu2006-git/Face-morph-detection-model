import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "model", "FINAL_WORKING_MODEL.h5")
MODEL_URL = "https://drive.google.com/uc?id=1GgDJt8PVoW4QQPRJ7xwm1Ry0aLs5bAa4"
IMAGE_SIZE = (299, 299)
THRESHOLD = 0.5