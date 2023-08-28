import numpy as np
import pandas as pd
from statsmodels.tsa.api import  SimpleExpSmoothing
from sklearn.feature_selection import SelectKBest, chi2
from ReadWriteClass import Reader
from Logger import log

class DataManager:
    """
    Type: A class for managing data preprocessing and feature engineering.

    Explanation: This class provides methods for preprocessing data, 
                 including smoothing, normalization, and feature engineering.

    
    Attributes: 1. df (pandas.DataFrame): The input DataFrame.
                2. smoothing_par: Parameter for smoothing (depends on smoothing_method).
                3. smoothing_method (str): The method for data smoothing.
                4. norm_name (str): The normalization method to use.
                5. fe_switch (bool): Whether to perform feature engineering.
    """

    def __init__(self, df, smoothing_par, smoothing_method, norm_name, fe_switch):
        """
        Input: 1. df (pandas.DataFrame): The input DataFrame.
               2. smoothing_par: Parameter for smoothing (depends on smoothing_method).
               3. smoothing_method (str): The method for data smoothing.
               4. norm_name (str): The normalization method to use.
               5. fe_switch (bool): Whether to perform feature engineering.
        Explanation: Initialize the DataManager object.

        """
        self.df = df
        self.smoothing_par = smoothing_par
        self.smoothing_method = smoothing_method
        self.norm_name = norm_name
        self.fe_switch = fe_switch

    def dataframe_manager(self):
        """
        Explanation: Apply preprocessing, normalization feature engineering on
                     the input DataFrame.
        output: 1. (pandas.DataFrame): The transformed DataFrame.
        """
        # Preprocessing part
        preprocessing_obj = Preprocessing(self.df, self.smoothing_par, self.smoothing_method)
        self.df = preprocessing_obj.dataframe_smoother()

        # Normalization part
        normalization_obj = Normalization(self.df.iloc[:, :-1], self.norm_name)
        self.df.iloc[:, :-1] = normalization_obj.method_selector()

        if self.fe_switch:
            # Feature engineering
            feature_engineering_obj = FeatureEngineering(self.df)
            self.df = feature_engineering_obj.dataframe_cropper(12)

        return self.df

class Preprocessing():
    """
    Type: A class for data preprocessing.
    Explanation: This class provides methods for cleaning, pruning, and smoothing a DataFrame.
    Attributes: 1. smoothing_par: Parameter for smoothing (depends on smoothing_method).
                2. smoothing_method (str): The method for data smoothing.
                3. df (pandas.DataFrame): The input DataFrame after cleaning.
    """

    def __init__(self, df, smoothing_par, smoothing_method):
        """    
        Input: 1. df (pandas.DataFrame): The input DataFrame.
               2. smoothing_par: Parameter for smoothing (depends on smoothing_method).
               3. smoothing_method (str): The method for data smoothing.
        Explanation: Initialize the Preprocessing object.
        """
        self.smoothing_par = smoothing_par
        self.smoothing_method = smoothing_method
        self.df = self.datframe_cleaner(df)

    def datframe_cleaner(self, df):
        """
        Input: 1. df (pandas.DataFrame): The input DataFrame.
        Explanation: Clean and preprocess the input DataFrame. This function prunes
                     unnecessary columns, changes the timestamp column to the index,
                     and fills missing values. 
        Output: 1. (pandas.DataFrame): The cleaned DataFrame.

        """
        # Make a copy of the dataset
        df_processed = df.copy()

        # change the type of the timestamp column
        df_processed['timestamp'] = pd.to_datetime(df_processed['timestamp'])

        # set timestamp column as the index
        df_processed.set_index('timestamp', inplace=True)

        # Drop redundant columns
        df_processed.drop(['sensor_15', 'sensor_50', 'sensor_51', 'Unnamed: 0'],
                           inplace = True,axis=1)

        # Fill the null values
        df_processed.iloc[:,:-1] = df_processed.iloc[:,:-1].fillna(method='bfill').fillna(method='ffill')

        return df_processed

    def dataframe_smoother(self):
        """
        Explanation: Apply a smoothing technique on the dataset. This function implements
                     either rolling mean or exponential smoothing based on the provided
                     smoothing method.  
        Output: 1. (pandas.DataFrame): The smoothed DataFrame.

        """
        df_copy = self.df.copy()

        # Slice the floating part
        float_df = self.df.iloc[:,:-1]

        if self.smoothing_method == 'rolling_mean':
            #calculate rolling mean
            smoothed_df = float_df.rolling(window=self.smoothing_par, min_periods=1).mean()

        else:
            #calculate exponential smoothing technique
            smoothed_dfs = {}

            for column in float_df.columns:
                model = SimpleExpSmoothing(np.array(float_df[column]))
                smoothed_model = model.fit(smoothing_level=self.smoothing_par, optimized=True,)
                smoothed_dfs[column] = smoothed_model.fittedvalues

            smoothed_df = pd.DataFrame(smoothed_dfs)

            df_copy.iloc[:, :49] = smoothed_df

        return df_copy

class Normalization():
    """
    Type: A class for data normalization.
    Explanation: This class provides methods for normalizing a DataFrame using different techniques.
    Attributes: 1. df (pandas.DataFrame): The input DataFrame.
                2. norm_name (str): The normalization method to use.
    """

    def __init__(self, df, norm_name):
        """
        Input: 1. df (pandas.DataFrame): The input DataFrame.
               2. norm_name (str): The normalization method to use.
        Explanation: Initialize the Normalization object.
        """
        self.df = df
        self.norm_name = norm_name

    def max_normalizer(self): 
        """
        Explanation: Apply 'max' normalization on the DataFrame.
        Output: (pandas.DataFrame): The normalized DataFrame.
        """
        df_normalized = self.df.apply(lambda x: x / x.abs().max())
        return df_normalized

    def min_max_normalizer(self):
        """
        Explanation: Apply 'min-max' normalization on the DataFrame.
        Output: (pandas.DataFrame): The normalized DataFrame.
        """
        df_normalized = self.df.apply(lambda x: (x - x.min()) / (x.max() - x.min()))
        return df_normalized

    def z_score_normalizer(self):
        """
        Explanation: Apply z-score normalization on the DataFrame.
        Output: (pandas.DataFrame): The normalized DataFrame.
        """
        df_normalized = self.df.apply(lambda x: (x - x.mean()) / x.std())
        return df_normalized

    def method_selector(self):
        """
        Explanation: Choose and apply the appropriate normalization method.
        Output: (pandas.DataFrame): The normalized DataFrame.
        """
        # make the function name
        method_name = f'{self.norm_name}_normalizer'
        normalization_method = getattr(self, method_name)

        # return the normalized dataframe
        return normalization_method()

class FeatureEngineering():
    """
    Type: A class for feature engineering.
    Explanation: This class provides methods for performing feature engineering on a DataFrame.
    Attributes: 1. df (pandas.DataFrame): The input DataFrame.
                2. selector: The SelectKBest model for feature selection.
    """
    def __init__(self, df):
        """
        Input: 1. df (pandas.DataFrame): The input DataFrame.
        Explanation: Initialize the FeatureEngineering object.
        """
        self.df = df
        self.selector = self.feature_engineering()
    
    def making_one_hot(self):
        """
        Explanation: Create one-hot encoded labels from the 'machine_status' column.
        Output: 1. (pandas.DataFrame): The one-hot encoded labels DataFrame.
        """
        # make one hot encoder
        status_series = self.df.machine_status
        one_hot = pd.get_dummies(status_series)
        one_hot = one_hot.astype(int)
        return one_hot

    def feature_engineering(self):
        """
        Explanation: Perform feature engineering using SelectKBest model.
        Output: 1. (sklearn.feature_selection.SelectKBest): The SelectKBest model.
        """
        float_df = self.df.iloc[:,:-1]

        # make one hot encoder
        one_hot = self.making_one_hot()

        # extract feature importance scores
        selector = SelectKBest(score_func=chi2)
        selector.fit(float_df, one_hot['NORMAL'])

        return selector

    def score_sorter(self):
        """
        Explanation: Sort feature importance scores in descending order.
        Output: 1. (dict): A dictionary of columns and their scores.
        """
        rank_dict = {}
        names = self.df.columns

        # make a dictionary of scores
        for number,_ in enumerate(self.selector.scores_):
            rank_dict[names[number]] = self.selector.scores_[number]

        # sort the scores
        rank_dict = dict(sorted(rank_dict.items(), key=lambda item: -1 * item[1]))

        return rank_dict

    def dataframe_cropper(self, slice_number):
        """
        Input: 1. slice_number (int): The number of columns to keep.
        Explanation: Crop the dataset to keep columns with the highest scores.
        Output: 1. (pandas.DataFrame): The cropped DataFrame.
        """
        # make the rank dictionary
        rank_dict = self.score_sorter()

        # make name list
        name_list = list(rank_dict.keys())[:slice_number]

        # crop the dataframe
        selected_df = self.df.iloc[:,:49].loc[:,name_list]
        selected_df['machine_status'] = self.df['machine_status']

        return selected_df

def test(raw_df_path, df_name):
    """
    Input: 1. raw_df_path (str): The path to the directory containing the raw DataFrame.
           2. df_name (str): The name of the raw DataFrame file.
    Explanation: Test the different stages of the DataManager class. This function
                 demonstrates how to use the DataManager class to preprocess a raw
                 DataFrame through various stages, including smoothing and normalization.
    """
    logger_obj = log('data_manager_test.log')
    reader_obj = Reader(logger_obj)

    # read a raw dataframe
    raw_df = reader_obj.dataframe_reader(raw_df_path, df_name)
    logger_obj.write_to_logger('Loaded the raw file')

    # transform the dataframe
    df_manager_obj = DataManager(raw_df,
                              smoothing_par=None,
                              smoothing_method='exponential',
                              norm_name='min_max',
                              fe_switch=False)  
    df_trans = df_manager_obj.dataframe_manager()
    logger_obj.write_to_logger('Received transformed data')

    logger_obj.write_to_logger(df_trans.head())

if __name__ == '__main__':
    test('raw_file_directory', 'sensor.csv')
    