import numpy as np
#from keras.layers import Dense, Activation, Flatten, Conv2D, Lambda
#from keras.layers import MaxPooling2D, Dropout
#from keras.utils import print_summary
#from keras.models import Sequential
#from keras.callbacks import ModelCheckpoint
#import keras.backend as K
import pickle
import tensorflow as tf
from tensorflow import keras

from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle


def keras_model(image_x, image_y):
    model = keras.models.Sequential()
    model.add(keras.layers.Lambda(lambda x: x / 127.5 - 1., input_shape=(image_x, image_y, 1)))
    model.add(keras.layers.Conv2D(32, (3, 3), padding='same'))
    model.add(keras.layers.Activation('relu'))
    model.add(keras.layers.MaxPooling2D((2, 2), padding='valid'))
    model.add(keras.layers.Conv2D(32, (3, 3), padding='same'))
    model.add(keras.layers.Activation('relu'))
    model.add(keras.layers.MaxPooling2D((2, 2), padding='valid'))

    model.add(keras.layers.Conv2D(64, (3, 3), padding='same'))
    model.add(keras.layers.Activation('relu'))
    model.add(keras.layers.MaxPooling2D((2, 2), padding='valid'))
    model.add(keras.layers.Conv2D(64, (3, 3), padding='same'))
    model.add(keras.layers.Activation('relu'))
    model.add(keras.layers.MaxPooling2D((2, 2), padding='valid'))

    model.add(keras.layers.Conv2D(128, (3, 3), padding='same'))
    model.add(keras.layers.Activation('relu'))
    model.add(keras.layers.MaxPooling2D((2, 2), padding='valid'))
    model.add(keras.layers.Conv2D(128, (3, 3), padding='same'))
    model.add(keras.layers.Activation('relu'))
    model.add(keras.layers.MaxPooling2D((2, 2), padding='valid'))

    model.add(keras.layers.Flatten())
    model.add(keras.layers.Dropout(0.5))
    model.add(keras.layers.Dense(1024))
    model.add(keras.layers.Dense(256))
    model.add(keras.layers.Dense(64))
    model.add(keras.layers.Dense(1))

    model.compile(optimizer=keras.optimizers.Adam(lr=0.0001), loss="mse")
    filepath = "models/Autopilot_10.h5"
    checkpoint = keras.callbacks.ModelCheckpoint(filepath, verbose=1, save_best_only=True)
    callbacks_list = [checkpoint]

    return model, callbacks_list


def loadFromPickle():
    with open("features", "rb") as f:
        features = np.array(pickle.load(f))
    with open("labels", "rb") as f:
        labels = np.array(pickle.load(f))

    return features, labels


def main():
    features, labels = loadFromPickle()
    features, labels = shuffle(features, labels)
    train_x, test_x, train_y, test_y = train_test_split(features, labels, random_state=0,
                                                        test_size=0.3)
    train_x = train_x.reshape(train_x.shape[0], 100, 100, 1)
    test_x = test_x.reshape(test_x.shape[0], 100, 100, 1)
    model, callbacks_list = keras_model(100, 100)
    model.fit(train_x, train_y, validation_data=(test_x, test_y), epochs=3, batch_size=32,
              callbacks=callbacks_list)
    model.summary()

    model.save('models/Autopilot_10.h5')


main()
#K.clear_session();
