import os
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
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
            os.chdir(file_directory)

            return load(model_name)

        except FileNotFoundError:
            print(f'model {model_name} not found.')
            return None

    def dataframe_writer(self, output_path, df, file_name):
        """
        This function save a file in a difinite output direction
        """
        output_dir = self.config[output_path]

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
        print(f'{model_name} saved successfully.')

    def plot_saver(self, output_path, plot, plot_name):

        output_dir = self.config[output_path]

        # Change the direction
        os.makedirs(output_dir, exist_ok=True)

        # make an agg figure
        plot.canvas.draw()

        # grab the pixel buffer and dump it into a numpy array
        X = np.array(plot.canvas.renderer.buffer_rgba())
        plt.imsave(plot_name, X)
        print(f'{plot_name} saved successfully.')

    def file_remover(self, target_path, file_name):
        target_dir = self.config[target_path]
        file_path = os.path.join(target_dir, file_name)

        if os.path.exists(file_path):
            os.remove(file_path)
            print(f'{file_name} removed successfully.')
        else:
            print(f'{file_name} not found.')

    def dictionary_saver(self, output_path, dictionary, dict_name):
        output_dir = self.config[output_path]

        # Change the direction
        os.makedirs(output_dir, exist_ok=True)
        with open(dict_name, 'wb') as name:
            pickle.dump(dictionary, name)
        print(f'{dict_name} saved successfully.')