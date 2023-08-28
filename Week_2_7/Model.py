import numpy as np
from ReadWriteClass import Reader


class Model():

    def __init__(self, input_dir, model_name):
        self.model = Reader().model_reader(input_dir, model_name)
    
    def predict(self, df):
        """
        This function predict for a specific dataset.
        """
        y_predict = self.model.predict(np.array(df))
        return y_predict