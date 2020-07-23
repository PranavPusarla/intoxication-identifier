import numpy as np
import tensorflow as tf
from tensorflow.keras import models, layers
import matplotlib.pyplot as  plt

image_data = np.load('../preprocessing/ImageData.npy')
labels = np.load('../preprocessing/labels.npy')
flipped_image_data = np.load('../imageAugmentation/flipped_ImageData.npy')
flipped_labels = np.load('../imageAugmentation/flipped_labels.npy')
mirrored_image_data = np.load('../imageAugmentation/mirrored_ImageData.npy')
mirrored_labels = np.load('../imageAugmentation/mirrored_labels.npy')

X = np.concatenate((image_data, flipped_image_data, mirrored_image_data), axis=0)
#print(X.shape)

y = np.concatenate((labels, flipped_labels, mirrored_labels), axis=0)
#print(y.shape)

model = models.Sequential()
model.add(layers.Conv2D(32, (3,3), activation='relu', input_shape=(128, 128, 3)))
model.add(layers.MaxPool2D(2,2))
model.add(layers.Conv2D(64, (3,3), activation='relu'))
model.add(layers.MaxPool2D(2,2))
model.add(layers.Conv2D(64, (3,3), activation='relu'))
model.add(layers.Flatten())
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dense(2))

model.compile(optimizer='adam', loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True), metrics=['accuracy'])
training_history = model.fit(X, y, epochs=11)

plt.plot(training_history.history['accuracy'], label='accuracy')
plt.xlabel("Epoch")
plt.ylabel("Accuracy")
plt.legend(loc='lower right')
plt.show()