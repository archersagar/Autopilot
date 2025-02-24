import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle
import tensorflow as tf
from tensorflow import keras
#from tensorflow.keras.layers import Input, Dense, Activation, Flatten, Conv2D, Lambda
#from keras.layers import MaxPooling2D, Dropout
#from tensorflow.python.keras.utils import print_summary
import tensorflow as tf
#from keras.models import Sequential
#from keras.callbacks import ModelCheckpoint
import pickle
#from keras.optimizers import Adam


def keras_model():
    model = keras.models.Sequential()
    model.add(keras.layers.Lambda(lambda x: x / 127.5 - 1., input_shape=(40, 40, 1)))

    model.add(keras.layers.Conv2D(32, (3, 3), padding='same'))
    model.add(keras.layers.Activation('relu'))
    model.add(keras.layers.MaxPooling2D((2, 2), padding='valid'))

    model.add(keras.layers.Conv2D(64, (3, 3), padding='same'))
    model.add(keras.layers.Activation('relu'))
    model.add(keras.layers.MaxPooling2D((2, 2), padding='valid'))

    model.add(keras.layers.Conv2D(128, (3, 3), padding='same'))
    model.add(keras.layers.Activation('relu'))
    model.add(keras.layers.MaxPooling2D((2, 2), padding='valid'))

    model.add(keras.layers.Flatten())
    model.add(keras.layers.Dropout(0.5))

    model.add(keras.layers.Dense(128))

    model.add(keras.layers.Dense(64))
    model.add(keras.layers.Dense(1))

    model.compile(optimizer=keras.optimizers.Adam(lr=0.0001), loss="mse")
    filepath = "Autopilot.h5"
    checkpoint1 = keras.callbacks.ModelCheckpoint(filepath, verbose=1, save_best_only=True)
    callbacks_list = [checkpoint1]

    return model, callbacks_list


def loadFromPickle():
    with open("features_40", "rb") as f:
        features = np.array(pickle.load(f))
    with open("labels", "rb") as f:
        labels = np.array(pickle.load(f))

    return features, labels


def augmentData(features, labels):
    features = np.append(features, features[:, :, ::-1], axis=0)
    labels = np.append(labels, -labels, axis=0)
    return features, labels


def main():
    features, labels = loadFromPickle()
    features, labels = augmentData(features, labels)
    features, labels = shuffle(features, labels)
    train_x, test_x, train_y, test_y = train_test_split(features, labels, random_state=0,
                                                        test_size=0.1)
    train_x = train_x.reshape(train_x.shape[0], 40, 40, 1)
    test_x = test_x.reshape(test_x.shape[0], 40, 40, 1)
    model, callbacks_list = keras_model()
    model.fit(train_x, train_y, validation_data=(test_x, test_y), epochs=5, batch_size=64,
              callbacks=callbacks_list)
    model.summary()
    model.save('Autopilot.h5')


main()
