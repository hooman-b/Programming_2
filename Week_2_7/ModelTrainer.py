import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.model_selection import GridSearchCV

# Internal Modules
from DataManager import DataManager
from ReadWriteClass import ReadWrite

class ModelTrainer():

    def __init__(self, df):
        self.df = df

    def multiple_grid_search(self, estimator_dict, scoring_list, cv_number, refit_method, data_dict):

        final_dict = {}

        for name in estimator_dict.keys():
            # Create the GridSearchCV object
            grid_search = GridSearchCV(estimator=estimator_dict[name][0], param_grid=estimator_dict[name][1],
                                        scoring=scoring_list, cv=cv_number, refit=refit_method)
            
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

        final_dict = self.multiple_grid_search(estimator_dict, scoring_list, 5, 'accuracy', data_dict)

        # Save the model
        read_write_obj.model_saver(final_dict['IsolationForest']['best_model'], 'if_model.joblib')
    
        return final_dict

if __name__ == '__main__':
    from sklearn.metrics import make_scorer, f1_score, accuracy_score
    read_write_obj = ReadWrite()
    df = read_write_obj.dataframe_reader('output_path','train_data')
    print(f'raw dataframe\n{df}')

    manager_obj = DataManager(df,
                              fill_method='ffill',
                              smoothing_par=None,
                              smoothing_method='exponential',
                              norm_name='min_max')
    df_trans = manager_obj.dataframe_manager()
    print(f'processed dataframe\n{df_trans}')
    y_train = [1 if element=='NORMAL' else -1 for element in df_trans.iloc[:,-1]]
    model_trainer_obj = ModelTrainer(df_trans)

    model_dict = model_trainer_obj.model_trainer()
    print(model_dict)
    y_pred = model_dict['IsolationForest']['best_model'].predict(df_trans.iloc[:,:-1])
    print(np.unique(y_pred))
    print(accuracy_score(y_train, y_pred))


