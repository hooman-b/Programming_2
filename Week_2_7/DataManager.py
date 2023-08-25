import pandas as pd
from statsmodels.tsa.api import  SimpleExpSmoothing

class DataManager():

    def __init__(self, df, norm_name, smoothing_par, smoothing_method):
        self.df = df

        self.norm_name = norm_name

        self.smoothing_par = smoothing_par
        self.smoothing_method = smoothing_method


class Normalization(DataManager):
      
    def max_norm(self): 
        return self.df.apply(lambda x: x / x.abs().max())

    def min_max_norm(self):
        return self.df.apply(lambda x: (x - x.min()) / (x.max() - x.min()))

    def z_score_norm(self):    
        return self.df.apply(lambda x: (x - x.mean()) / x.std())

    def method_selector(self):
        """
        input: 1- method_name: this string determines the method's type.
        explanation: This function chooses the right endmember extraction method based
                     on the input name. And, return the endmembers based on the method.
        output: 1- an endmember method
        """
        # make the function name
        method_name = f'{self.norm_name}_norm'
        normalization_method = getattr(self, method_name)
        # return the spectrum
        return normalization_method()


class Prprocessing(DataManager):

    def datframe_pruner(self):
        # Drop redundant columns
        self.df.drop(['sensor_15', 'sensor_50', 'sensor_51'],inplace = True,axis=1)
        # Fill the null values
        self.df.iloc[:,:-1] = self.df.iloc[:,:-1].fillna(method='bfill')

    def smoothing_data(self):
        float_df = self.df.iloc[:,:49]

        if self.smoothing_method == 'rolling_mean':
            #calculate rolling mean
            smoothed_df = float_df.rolling(window=self.smoothing_par, min_periods=1).mean()

        else:
            #calculate exponential smoothing technique
            smoothed_dfs = {}

            for column in float_df.columns:
                model = SimpleExpSmoothing(float_df[column])
                smoothed_model = model.fit(smoothing_level=self.smoothing_par, optimized=True,)
                smoothed_dfs[column] = smoothed_model.fittedvalues

            smoothed_df = pd.DataFrame(smoothed_dfs)

        self.df.iloc[:, :49] = smoothed_df

class FeatureEngineering():
    pass
