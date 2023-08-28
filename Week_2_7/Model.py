import numpy as np
from ReadWriteClass import Reader

class Model:
    """
    type: A class for making predictions using a pre-trained model.
    explanation: This class provides methods to load a trained model and make predictions
                 on new data.
    attributes: 1. logger_obj (Logger): An instance of the Logger class for logging.
                2. model (object): The pre-trained model loaded from the file.
    """

    def __init__(self, input_dir, model_name, logger_obj):
        """
        inpute: 1. input_dir (str): The directory containing the trained model file.
                2. model_name (str): The name of the trained model file.
                3. logger_obj (Logger): An instance of the Logger class for logging.
        explanation: Initialize the Model object.
        """
        self.logger_obj = logger_obj
        self.model = Reader(self.logger_obj).model_reader(input_dir, model_name)

    def predict(self, df):
        """
        input: df (pandas.DataFrame): The input dataset for making predictions.
        explanation: Predict labels for a given dataset using the pre-trained model.
        output: numpy.ndarray: An array of predicted labels.
        """
        y_predict = self.model.predict(np.array(df))
        return y_predict
