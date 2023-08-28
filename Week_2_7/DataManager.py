# General libraries
import os
import yaml
import numpy as np
import pandas as pd
from statsmodels.tsa.api import  SimpleExpSmoothing
from sklearn.feature_selection import SelectKBest, chi2

class DataManager():

    def __init__(self, df, fill_method, smoothing_par, smoothing_method, norm_name):
        self.df = df

        # Preprocessing parameters
        self.fill_method = fill_method
        self.smoothing_par = smoothing_par
        self.smoothing_method = smoothing_method

        # Normalization parameters
        self.norm_name = norm_name

    def dataframe_manager(self):
        """
        This function implements all the preprocessing steps on the dataframe
        and returns the transformed dataset to the main function.
        """
        # Preprocessing part
        preprocessing_obj = Preprocessing(self.df, self.fill_method, self.smoothing_par,
                                         self.smoothing_method)
        self.df = preprocessing_obj.dataframe_smoother()

        # Normalization part
        normalization_obj = Normalization(self.df.iloc[:,:-1], self.norm_name)
        self.df.iloc[:,:-1] = normalization_obj.method_selector()

        # Feature engineering
        feature_engineering_obj = FeatureEngineering(self.df)
        self.df = feature_engineering_obj.dataframe_cropper(12)

        return self.df

class Preprocessing():

    def __init__(self, df, fill_method, smoothing_par, smoothing_method):
        self.fill_method = fill_method
        self.smoothing_par = smoothing_par
        self.smoothing_method = smoothing_method
        self.df = self.datframe_cleener(df)

    def datframe_cleener(self, df):
        """
        This function prune (drop) the necessary data columns and fill the Nan values
        """
        # Make a copy of the dataset
        df_processed = df.copy()

        # change the type of the timestamp column
        df_processed['timestamp'] = pd.to_datetime(df_processed['timestamp'])

        # set timestamp column as the index
        df_processed.set_index('timestamp', inplace=True)

        # Drop redundant columns
        df_processed.drop(['sensor_15', 'sensor_50', 'sensor_51', 'Unnamed: 0'], inplace = True,axis=1)

        # Fill the null values
        df_processed.iloc[:,:-1] = df_processed.iloc[:,:-1].fillna(method=self.fill_method)

        return df_processed

    def dataframe_smoother(self):
        """
        This function implements a smoothing technique on the dataset
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

    def __init__(self, df, norm_name):
        self.df = df
        self.norm_name = norm_name

    def max_normalizer(self): 
        """
        This function returns 'max' normalization
        """
        df_normalized = self.df.apply(lambda x: x / x.abs().max())
        return df_normalized

    def min_max_normalizer(self):
        """
        This function returns 'min_max normalization
        """
        df_normalized = self.df.apply(lambda x: (x - x.min()) / (x.max() - x.min()))
        return df_normalized

    def z_score_normalizer(self):
        """
        This function returns z-score normalization
        """
        df_normalized = self.df.apply(lambda x: (x - x.mean()) / x.std())
        return df_normalized

    def method_selector(self):
        """
        input: 1- method_name: this string determines the method's type.
        explanation: This function chooses the right endmember extraction method based
                     on the input name. And, return the endmembers based on the method.
        output: 1- an endmember method
        """
        # make the function name
        method_name = f'{self.norm_name}_normalizer'
        normalization_method = getattr(self, method_name)

        # return the normalized dataframe
        return normalization_method()

class FeatureEngineering():

    def __init__(self, df):
        self.df = df
        self.selector = self.feature_engineering()
    
    def making_one_hot(self):
        """
        This function make one_hot encoder from label column
        """
        # make one hot encoder
        status_series = self.df.machine_status
        one_hot = pd.get_dummies(status_series)
        one_hot = one_hot.astype(int)
        return one_hot

    def feature_engineering(self):
        """
        This function implements SelectKBest model on the dataset
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
        This function make a sorted dictionary of the columns and their
        scores in an ascending manner
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
        This function crops the columns in the dataset with the highest
        scores in another dataset
        """
        # make the rank dictionary
        rank_dict = self.score_sorter()

        # make name list
        name_list = list(rank_dict.keys())[:slice_number]

        # crop the dataframe
        selected_df = self.df.iloc[:,:49].loc[:,name_list]
        selected_df['machine_status'] = self.df['machine_status']

        return selected_df

if __name__ == '__main__':

    with open("config.yaml", "r") as inputFile:
        config = yaml.safe_load(inputFile)

    file_directory, file_name,a,b = config.values()
    os.chdir(a)
    df = pd.read_csv(b)#.drop('Unnamed: 0', axis=1)

    # change the type of the timestamp column
    #df['timestamp'] = pd.to_datetime(df['timestamp'])

    # set timestamp column as the index
    #df.set_index('timestamp', inplace=True)
    manager_obj = DataManager(df,
                              fill_method='ffill',
                              smoothing_par=None,
                              smoothing_method='exponential',
                              norm_name='min_max')
    df_trans = manager_obj.dataframe_manager()
    print(df_trans.head())
    