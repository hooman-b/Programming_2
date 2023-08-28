import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.model_selection import GridSearchCV
from DataManager import DataManager
from ReadWriteClass import Reader, Writer
from Logger import log

class ModelTrainer():
    """
    Type: A class for training models using grid search and evaluating their performance.
    Explanation: This class provides methods to perform a grid search over hyperparameters,
                 train and evaluate models, and return the best-performing model along with
                 its parameters.
    Attributes: 1. df (pandas.DataFrame): The input dataset containing features and labels.
    """

    def __init__(self, df):
        """
        Input: 1. df (pandas.DataFrame): The input dataset containing features and labels.
        Explanation: Initialize a ModelTrainer object.
        """
        self.df = df

    def multiple_grid_search(self, estimator_dict, scoring_list, cv_number, refit_method, data_dict):
        """
        Input: 1. estimator_dict (dict): A dictionary containing estimator names as keys and
                                   a list of estimator objects and their parameter grids as values.
               2. scoring_list (list): List of scoring metrics for evaluation.
               3. cv_number (int): Number of cross-validation folds.
               4. refit_method (str): Name of the scoring metric to use for refitting the best
                                      model.
               5. data_dict (dict): A dictionary containing input data and labels as 'x' and 'y'
                                    keys.
        Explanation: Perform grid search over multiple estimators and return the best models.
        Output: 1. (dict): A dictionary containing the best models, their parameters, and scores
                           for each estimator.
        """
        final_dict = {}

        for name in estimator_dict.keys():
            # Create the GridSearchCV object
            grid_search = GridSearchCV(estimator=estimator_dict[name][0],
                                        param_grid=estimator_dict[name][1],
                                        scoring=scoring_list, cv=cv_number,
                                        refit=refit_method)

            # Fit the the best model to the data
            grid_search.fit(data_dict['x'], data_dict['y'])

            # Save the best estimator for each model
            final_dict[name] = {'best_model': grid_search.best_estimator_,
                                'best_parameters': grid_search.best_params_,
                                'best_score': grid_search.best_score_}

        # order the dictionary based on the magnitude of the scores
        final_dict = dict(sorted(final_dict.items(), key=lambda item: -1 * item[1]['best_score']))
        return final_dict

    def model_trainer(self):
        """
        Explanation: Train and evaluate models using the input dataset and return the
                     best-performing model.
        Output: 1. (dict): A dictionary containing the best model, its parameters, and scores.
        """
        # Convert label column into 1 and -1, ro make it comparable to the model 
        y_train = [1 if element=='NORMAL' else -1 for element in self.df.iloc[:,-1]]
        X = np.array(self.df.iloc[:,:-1])

        # Make data dictionary
        data_dict =  {'x': X,
                    'y': y_train}

        # Find the outlier fraction in the dataset
        normal_rows = self.df[self.df['machine_status']=='NORMAL']
        outliers_fraction = 1 - (len(normal_rows)/(len(self.df)))

        # make parameters dictionaries for Isolation Forest
        if_param= {
            'n_estimators': [50, 100, 200],
            'max_samples': [0.5, 0.8, 1.0],
            'contamination': [outliers_fraction],
            'max_features': [0.5, 0.8, 1.0],
            'n_jobs': [-1]
            }

        # Scoring list
        scoring_list = {'roc_auc', 'accuracy', 'f1'}

        # Make estimator dictionary
        estimator_dict={'IsolationForest': [IsolationForest(), if_param]}

        final_dict = self.multiple_grid_search(estimator_dict, scoring_list, 5, 'accuracy',
                                                data_dict)
        return final_dict

def main(df_path, df_name, model_path):
    """
    Input: 1. df_path (str): The path to the directory containing the raw dataset.
           2. df_name (str): The filename of the raw dataset.
           3. model_path (str): The path to the directory where the trained model will
                                be saved.
    Explanation: The main function that reads, preprocesses, trains, and saves a
                 machine learning model.
    """
    logger_obj = log('model_trainer.log')
    reader_obj = Reader(logger_obj)
    writer_obj = Writer(logger_obj)

    # Read the raw dataset
    df = reader_obj.dataframe_reader(df_path, df_name)
    logger_obj.write_to_logger('Loaded the file')
    logger_obj.write_to_logger(f'raw dataframe\n{df.head()}')

    # transform the raw dataset
    df_manager_obj = DataManager(df,
                              smoothing_par=None,
                              smoothing_method='exponential',
                              norm_name='min_max',
                              fe_switch=False)
    df_trans = df_manager_obj.dataframe_manager()
    logger_obj.write_to_logger('Received transformed data')
    logger_obj.write_to_logger(f'processed dataframe\n{df_trans.head()}')

    # Train a model
    model_trainer_obj = ModelTrainer(df_trans)
    model_dict = model_trainer_obj.model_trainer()
    logger_obj.write_to_logger('Trained the model')

    # Save the model
    writer_obj.model_writer(model_path, model_dict['IsolationForest']['best_model'], 'if_model.joblib')
    logger_obj.write_to_logger('Saved the model')

if __name__ == '__main__':
    main('divided_data_directory','df_train.csv', 'model_directory')