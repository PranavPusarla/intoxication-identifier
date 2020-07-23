import numpy as np
import cv2
from PIL import Image, ImageOps


image = Image.open("../croppedImages/drunk27_0.jpg")
image.show()
im_flipped = ImageOps.flip(image)
im_flipped.show()
im_mirror = ImageOps.mirror(image)
im_mirror.show()