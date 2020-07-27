import numpy as np
import tensorflow as tf
from tensorflow.keras import models, layers
import matplotlib.pyplot as  plt
from PIL import Image

image_data = np.load('../preprocessing/ImageData.npy')
labels = np.load('../preprocessing/labels.npy')
flipped_image_data = np.load('../imageAugmentation/flipped_ImageData.npy')
flipped_labels = np.load('../imageAugmentation/flipped_labels.npy')
mirrored_image_data = np.load('../imageAugmentation/mirrored_ImageData.npy')
mirrored_labels = np.load('../imageAugmentation/mirrored_labels.npy')
blurred_image_data = np.load('../imageAugmentation/blurred_ImageData.npy')
blurred_labels = np.load('../imageAugmentation/blurred_labels.npy')

train_test_split = 0.8 #training percentage
image_data_train = image_data[:int(image_data.shape[0]*(train_test_split))]
image_data_test = image_data[int(image_data.shape[0]*train_test_split):]
labels_train = labels[:int(labels.shape[0]*(train_test_split))]
labels_test = labels[int(labels.shape[0]*train_test_split):]
flipped_image_data_train = flipped_image_data[:int(flipped_image_data.shape[0]*(train_test_split))]
flipped_image_data_test = flipped_image_data[int(flipped_image_data.shape[0]*train_test_split):]
flipped_labels_train = flipped_labels[:int(flipped_labels.shape[0]*(train_test_split))]
flipped_labels_test = flipped_labels[int(flipped_labels.shape[0]*train_test_split):]
mirrored_image_data_train = mirrored_image_data[:int(mirrored_image_data.shape[0]*(train_test_split))]
mirrored_image_data_test = mirrored_image_data[int(mirrored_image_data.shape[0]*train_test_split):]
mirrored_labels_train = mirrored_labels[:int(mirrored_labels.shape[0]*(train_test_split))]
mirrored_labels_test = mirrored_labels[int(mirrored_labels.shape[0]*train_test_split):]
blurred_image_data_train = blurred_image_data[:int(blurred_image_data.shape[0]*(train_test_split))]
blurred_image_data_test = blurred_image_data[int(blurred_image_data.shape[0]*train_test_split):]
blurred_labels_train = blurred_labels[:int(blurred_labels.shape[0]*(train_test_split))]
blurred_labels_test = blurred_labels[int(blurred_labels.shape[0]*train_test_split):]

X_train = np.concatenate((image_data_train, flipped_image_data_train, mirrored_image_data_train, blurred_image_data_train), axis=0)
X_test = np.concatenate((image_data_test, flipped_image_data_test, mirrored_image_data_test, blurred_image_data_test), axis=0)
# for i in range(5):
#     img = Image.fromarray((X_train[i+250] * 255).astype(np.uint8), mode='RGB')
#     img.show()
# print(X_train.shape)

y_train = np.concatenate((labels_train, flipped_labels_train, mirrored_labels_train, blurred_labels_train), axis=0)
y_test = np.concatenate((labels_test, flipped_labels_test, mirrored_labels_test, blurred_labels_test), axis=0)
# print(y_train.shape)

model = models.Sequential()
model.add(layers.Conv2D(32, (3,3), activation='relu', input_shape=(128, 128, 3)))
model.add(layers.MaxPool2D(2,2))
model.add(layers.Conv2D(64, (3,3), activation='relu'))
model.add(layers.MaxPool2D(2,2))
model.add(layers.Conv2D(128, (3,3), activation='relu'))
model.add(layers.MaxPool2D(2,2))
model.add(layers.Conv2D(128, (3,3), activation='relu'))
model.add(layers.Flatten())
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dropout(0.1))
model.add(layers.Dense(16, activation='relu'))
model.add(layers.Dense(2, activation='softmax'))

model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=False),
              metrics=['accuracy'])
training_history = model.fit(X_train, y_train, epochs=20, validation_data=(X_test, y_test))
predictions = model.predict(X_test)
error = []
for i in range(predictions.shape[0]):
    if y_test[i] == 1:
        error.append(1 - predictions[i][1])
    else:
        error.append(1 - predictions[i][0])
# for i in range(len(error)):
#     if error[i] > 0.5:
#         array = X_test[i]
#         img = Image.fromarray(array, 'RGB')
#         img.show()
results = model.evaluate(X_test, y_test)
print('\nTesting Accuracy: {:.2f}%'.format(results[1]*100))

plt.plot(training_history.history['accuracy'], label='accuracy')
plt.plot(training_history.history['val_accuracy'], label='val_accuracy')
plt.xlabel("Epoch")
plt.ylabel("Accuracy")
plt.legend(loc='lower right')
plt.show()