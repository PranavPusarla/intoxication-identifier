from os import listdir

import numpy as np
import cv2
from numpy import asarray
from PIL import Image

#display some images
# count = 0
# for filename in listdir('croppedImages'):
#     if count < 5:
#         print(filename)
#         img = Image.open('../croppedImages/' + filename)
#         img.show()
#     count += 1

img_data = []
labels = []
for filename in listdir('croppedImages'):
    if filename[0] == 'd':
        img = Image.open('croppedImages/' + filename)
        data = np.asarray(img)
        resized_image = cv2.resize(data, dsize=(128,128), interpolation=cv2.INTER_CUBIC)
        if filename[8] == '0' or filename[8] == '1':
            labels.append(0)
        else:
            labels.append(1)
        if resized_image.shape[2] == 4:
            resized_image = resized_image[:,:,:-1]
        resized_image = resized_image / 255.0
        img_data.append(resized_image)

img_data = np.array(img_data)
np.save('preprocessing/labels', labels)
np.save('preprocessing/ImageData', img_data)

