from ReadWriteClass import ReadWrite
from ConfigReader import ConfigReader

class Model():

    def __init__(self, input_dir, model_name):
        self.model = ReadWrite().model_reader(input_dir, model_name)
    
    def predict(self, df):
        y_predict = self.model.predict(df)
        return y_predict