import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "model", "FINAL_CLEAN_RENDER.h5")

MODEL_URL = "https://drive.google.com/uc?id=19xVm_Zn9tObOXwGRjB6ycowpWJOibGbp"
IMAGE_SIZE = (299, 299)
THRESHOLD = 0.5