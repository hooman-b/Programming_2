import os
import pandas as pd
from joblib import dump, load
from ConfigReader import ConfigReader

class ReadWrite():
    config = ConfigReader()

    def dataframe_reader(self, input_dir, file_name):
        """
        This function open a saved dataframe
        """
        try:
            # read the dataframe
            file_directory = self.config[input_dir]
            file_name = self.config[file_name]
            os.chdir(file_directory)

            return pd.read_csv(file_name)

        except FileNotFoundError:
            print(f'file {file_name} not found.')
            return None

    def model_reader(self, input_dir, model_name):
        """
        This function reads a model from a specific directory
        """
        try:
            # read the model
            file_directory = self.config[input_dir]
            model_name = self.config[model_name]
            os.chdir(file_directory)

            return load(model_name)

        except FileNotFoundError:
            print(f'model {model_name} not found.')
            return None

    def dataframe_writer(self, df, file_name):
        """
        This function save a file in a difinite output direction
        """
        output_dir = self.config['output_path']

        # Change the direction
        os.makedirs(output_dir, exist_ok=True)

        # save the dataframe
        df.to_csv(os.path.join(output_dir, file_name))
        print(f'{file_name} written successfully.')
    
    def model_saver(self, model, model_name):
        output_dir = self.config['output_path']

        # Change the direction
        os.makedirs(output_dir, exist_ok=True)
        dump(model, model_name)

