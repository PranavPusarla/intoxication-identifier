from os import listdir

import numpy as np
import cv2
from PIL import Image, ImageOps

img_data = []
labels = []
for filename in listdir('../croppedImages'):
    if filename[0] == 'd':
        image = Image.open('../croppedImages/' + filename)
        im_mirrored = ImageOps.mirror(image)
        data = np.asarray(im_mirrored)
        resized_image = cv2.resize(data, dsize=(128, 128), interpolation=cv2.INTER_CUBIC)
        if filename[8] == '0' or filename[8] == '1':
            labels.append(0)
        else:
            labels.append(1)
        if resized_image.shape[2] == 4:
            resized_image = resized_image[:,:,:-1]
        resized_image = resized_image / 255.0
        img_data.append(resized_image)

img_data = np.array(img_data)

np.save('mirrored_labels', labels)
np.save('mirrored_ImageData', img_data)