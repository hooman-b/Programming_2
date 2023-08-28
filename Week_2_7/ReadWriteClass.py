import os
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from joblib import dump, load
from ConfigReader import ConfigReader

class Reader():
    config = ConfigReader()

    def dataframe_reader(self, input_dir, file_name):
        """
        This function open a saved dataframe
        """
        try:
            # read the dataframe
            os.chdir(self.config[input_dir])
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
            os.chdir(self.config[input_dir])
            return load(model_name)

        except FileNotFoundError:
            print(f'model {model_name} not found.')
            return None


class Writer():
    config = ConfigReader()

    def directory_maker(self, directory):
        try:

            os.makedirs(directory)
            os.chdir(directory)
            print(f'Directory {directory} created successfully')

        except OSError:
            os.chdir(directory)
            print(f'Directory {directory} has already created')

    def dataframe_writer(self, output_path, df, file_name):
        """
        This function save a datframe in a difinite output direction
        """
        self.directory_maker(self.config[output_path])

        # save the dataframe
        df.to_csv(os.path.join(self.config[output_path], file_name))

    def model_writer(self, output_path, model, model_name):
        """
        This function save a trained model in a difinite output direction
        """
        self.directory_maker(self.config[output_path])

        # save the model
        dump(model, model_name)

    def plot_writer(self, output_path, plot, plot_name):
        """
        This function save a plot in a difinite output direction
        """
        self.directory_maker(self.config[output_path])

        # make an agg figure
        plot.canvas.draw()

        # grab the pixel buffer and dump it into a numpy array
        X = np.array(plot.canvas.renderer.buffer_rgba())
        plt.imsave(plot_name, X)

    def dictionary_writer(self, output_path, dictionary, dict_name):
        """
        This function write a dictionary in a difinite output direction
        """
        self.directory_maker(self.config[output_path])

        # write a dictionary.pickle file
        with open(dict_name, 'wb') as name:
            pickle.dump(dictionary, name)

    def file_remover(self, target_path, file_name):
        """
        This function removes a file in a difinite output direction
        """
        self.directory_maker(self.config[target_path])
    
        # Try to remove the file from the target directory
        try:
            os.remove(os.path.join(self.config[target_path], file_name))
        except FileNotFoundError:
            print(f'{file_name} not found.')

        #if os.path.exists(file_path):
        #    os.remove(file_path)

        #else:
        #    print(f'{file_name} not found.')


