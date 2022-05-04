import tensorflow as tf
import pandas as pd
import pickle


class ChurnModel:

    def __init__(self, path):
        self.model = tf.keras.models.load_model(path + '/model.h5')
        self.preprocessor = pickle.load(open(path + '/preprocessing.pkl', 'rb'))

    def __call__(self, x: pd.DataFrame):
        return self.model(self.preprocessor.transform(x))
