import numpy as np
import tensorflow as tf
from tensorflow.python.keras import Input, Model
from tensorflow.python.keras.layers import LSTM, Concatenate, Permute, Reshape

from config import Config
from data_loader import get_np_dataset

flags = tf.app.flags
FLAGS = flags.FLAGS

flags.DEFINE_string('config', 'conf/SML2010.json', 'Path to json file with the configuration to be run')

config = Config.from_file(FLAGS.config)
# set seeds for 'reproducibility'
tf.set_random_seed(config.seed)
np.random.seed(config.seed)

X_t, y_t = get_np_dataset(config)
X = Input(shape=(config.n, config.T))
past = Input(shape=(config.T,))
past_r = Reshape((1, config.T))(past)
z = Concatenate(axis=1)([X, past_r])
z = Permute((2, 1))(z)
z = LSTM(1)(z)

model = Model(inputs=[X, past], outputs=z)
model.compile(loss='mse', optimizer='adam', metrics=['mae'])
model.summary()

y_tt = y_t
y_t = np.copy(y_t[:, -1])
y_tt[:, -1] = 0

model.fit(x=[X_t, y_tt], y=y_t, epochs=100, batch_size=128)
