import numpy as np
from PIL import Image
from config import IMAGE_SIZE

def preprocess_image(image):
    image = image.resize(IMAGE_SIZE)
    image = np.array(image) / 255.0
    image = np.expand_dims(image, axis=0)
    return image