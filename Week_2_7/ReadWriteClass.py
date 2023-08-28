import os
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from joblib import dump, load
from ConfigReader import ConfigReader

class Reader():
    """
    Type: this class is a normal class.
    Explanation: The Reader class provides methods to read saved dataframes and models
                 from specified directories.
    Attributes: 1. config (ConfigReader): A ConfigReader object that provides configuration
                                          settings.
    """
    config = ConfigReader()

    def __init__(self, logger_obj):
        """
        Input: 1. logger_obj: An instance of a logger object to log error messages.
        Explanation: Initializes a new instance of the Reader class.
        """
        self.logger_obj = logger_obj

    def dataframe_reader(self, input_dir, file_name):
        """
        Input: 1. input_dir (str): The name of the configuration key containing the
                                   directory path.
            2. file_name (str): The name of the dataframe file to read.
        Explanation: Reads a saved dataframe from a specified directory.
        Output: 1. pd.DataFrame: The loaded dataframe if successful, None if the file
                                 is not found.
        """
        try:
            # read the dataframe
            os.chdir(self.config[input_dir])
            return pd.read_csv(file_name)

        except FileNotFoundError:
            self.logger_obj.error_to_logger(f'file {file_name} not found.')
            return None

    def model_reader(self, input_dir, model_name):
        """
        Input: 1. input_dir (str): The name of the configuration key containing the
                                   directory path.
               2. model_name (str): The name of the model file to read.
        Explanation: Reads a saved model from a specified directory.
        Output: 1. object: The loaded model if successful, None if the model file is not
                           found.
        """
        try:
            # read the model
            os.chdir(self.config[input_dir])
            return load(model_name)

        except FileNotFoundError:
            self.logger_obj.error_to_logger(f'model {model_name} not found.')
            return None


class Writer():
    """
    Type: This class is a normal function
    Explanation: The Writer class provides methods for creating and saving various types
                 of data, including dataframes, models, plots, dictionaries, and removing files.
    Attributes: 1. config (ConfigReader): A ConfigReader object that provides configuration
                                          settings.
    """
    config = ConfigReader()

    def __init__(self, logger_obj):
        """
        Input: 1. logger_obj: An instance of a logger object to log messages.
        Explanation: Initializes a new instance of the Writer class.
        """
        self.logger_obj = logger_obj

    def directory_maker(self, directory):
        """
        Explanation: Creates a directory if it doesn't exist.

        Args:
            directory (str): The directory to create.
        """
        try:
            os.makedirs(directory)
            os.chdir(directory)
            self.logger_obj.write_to_logger(f'Directory {directory} created successfully')

        except OSError:
            os.chdir(directory)
            self.logger_obj.error_to_logger(f'Directory {directory} has already created')


    def dataframe_writer(self, output_path, df, file_name):
        """
        Input: 1. output_path (str): The name of the configuration key containing
                                     the directory path.
               2. df (pd.DataFrame): The dataframe to save.
               3. file_name (str): The name of the output file.
        """
        self.directory_maker(self.config[output_path])
        # save the dataframe
        df.to_csv(os.path.join(self.config[output_path], file_name))


    def model_writer(self, output_path, model, model_name):
        """
        Input: 1. output_path (str): The name of the configuration key containing
                                     the directory path.
               2. model (object): The trained model to save.
               3. model_name (str): The name of the output model file.
        """
        self.directory_maker(self.config[output_path])
        # save the model
        dump(model, model_name)


    def plot_writer(self, output_path, plot, plot_name):
        """
        Input: 1. output_path (str): The name of the configuration key containing
                                     the directory path.
               2. plot: The plot object to save.
               3. plot_name (str): The name of the output plot file.
        """
        self.directory_maker(self.config[output_path])
        # make an agg figure
        plot.canvas.draw()
        # grab the pixel buffer and dump it into a numpy array
        X = np.array(plot.canvas.renderer.buffer_rgba())
        plt.imsave(plot_name, X)


    def dictionary_writer(self, output_path, dictionary, dict_name):
        """
        Input: 1. output_path (str): The name of the configuration key containing the
                                     directory path.
               2. dictionary (dict): The dictionary to write.
               3. dict_name (str): The name of the output dictionary file.
        """
        self.directory_maker(self.config[output_path])

        # write a dictionary.pickle file
        with open(dict_name, 'wb') as name:
            pickle.dump(dictionary, name)

    def file_remover(self, target_path, file_name):
        """
        Input: 1. target_path (str): The name of the configuration key containing
                                     the directory path.
               2. file_name (str): The name of the file to remove.
        """
        self.directory_maker(self.config[target_path])

        # Try to remove the file from the target directory
        try:
            os.remove(os.path.join(self.config[target_path], file_name))
        except FileNotFoundError:
            self.logger_obj.error_to_logger(f'{file_name} not found.')
            return None