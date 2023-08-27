from ReadWriteClass import ReadWrite


class Model():

    def __init__(self, input_dir, model_name):
        self.model = ReadWrite().model_reader(input_dir, model_name)
    
    def predict(self, df):
        """
        This function predict for a specific dataset.
        """
        y_predict = self.model.predict(df)
        return y_predict