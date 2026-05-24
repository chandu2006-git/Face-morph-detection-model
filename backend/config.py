import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "../model/inception_model.h5")

IMAGE_SIZE = (224, 224)
THRESHOLD = 0.5