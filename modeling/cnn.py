import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Flatten, Dense, Dropout, BatchNormalization
from tensorflow.keras.layers import Conv2D, MaxPool2D, ZeroPadding2D

from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import optimizers

import numpy as np
import matplotlib.pyplot as plt

from os import listdir


img_width = 128
img_height = 128

#Adding image augmentation
'''
datagen = ImageDataGenerator(rotation_range=15,
                             width_shift_range=0.2,
                             height_shift_range=0.2,
                             rescale=1/255.0,
                             shear_range=0.2,
                             horizontal_flip=True,
                             fill_mode='nearest',
                             validation_split=0.2)
'''

datagen = ImageDataGenerator(rescale=1/255.0, validation_split=0.2)
train_data_generator = datagen.flow_from_directory(directory='dataset',
                                                   target_size = (img_width, img_height),
                                                   class_mode='binary',
                                                   batch_size=15,
                                                   subset='training')

validation_data_generator = datagen.flow_from_directory(directory='dataset',
                                                   target_size = (img_width, img_height),
                                                   class_mode='binary',
                                                   batch_size=15,
                                                   subset='validation')

#Building the CNN
model = Sequential()

model.add(Conv2D(64, (3,3), input_shape=(img_width, img_height, 3), activation='relu'))
model.add(MaxPool2D(2, 2))
#model.add(Dropout(0.2))

model.add(Conv2D(32, (3, 3), activation='relu'))
model.add(MaxPool2D(2, 2))
#model.add(Dropout(0.3))

model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPool2D(2, 2))
#model.add(Dropout(0.3))

model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPool2D(2, 2))

model.add(Conv2D(128, (3, 3), activation='relu'))
#model.add(MaxPool2D(2, 2))

model.add(Flatten())

#model.add(Dense(512, activation='relu'))

model.add(Dense(256, activation='relu'))

model.add(Dense(128, activation='relu'))

model.add(Dense(64, activation='relu'))

model.add(Dense(32, activation='relu'))

model.add(Dense(1, activation='sigmoid'))

print(model.summary())

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
history = model.fit_generator(generator=train_data_generator,
                              steps_per_epoch=len(train_data_generator),
                              epochs=20,
                              validation_data=validation_data_generator,
                              validation_steps=len(validation_data_generator))
