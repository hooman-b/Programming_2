# pylint: disable=E1101
import os
import time
from ConfigReader import ConfigReader
from MyWatchdog import DataDirectoryWatcher
from ReadWriteClass import ReadWrite
from DataManager import DataManager
from ModelEvaluator import ModelEvaluator
from Model import Model
from Plotter import Plotter
from Logger import log

class Main():

    config = ConfigReader()

    # Function to process the newly added data file
    def main(self, file_name):
        """
        This is the main function of the program that implement all
        the process on a new observed dataset.
        """
        time.sleep(10)

        # make logging 
        name = os.path.splitext(file_name)
        logger = log('output_directory', f'log_{name}')

        # Print the new file path
        print(f'Found new data file: {file_name}')
        logger.write_to_logger(f'Found new data file: {file_name}')
    
        # make the dataframe
        read_write_obj = ReadWrite()
        raw_df = read_write_obj.dataframe_reader('target_directory', file_name)
        logger.write_to_logger('Loaded the file')

        # Transform the raw dataframe
        data_manager_obj = DataManager(raw_df,
                                fill_method='ffill',
                                smoothing_par=None,
                                smoothing_method='exponential',
                                norm_name='min_max')

        trans_df = data_manager_obj.dataframe_manager()
        logger.write_to_logger('Received transformed data')

        # Call the trained model
        model = Model('model_directory', 'if_model.joblib')

        # Predict the new labels
        y_pred = model.predict(trans_df.iloc[:, :-1])
        logger.write_to_logger('Received predicions')

        # Save the predicted column in the transform dataframe
        trans_df['IsolatedForest'] = y_pred
        logger.write_to_logger('Add predicions to the dataset')

        # Make a dictionary of evaluation metrics
        evaluator_obj = ModelEvaluator(trans_df['machine_status'], y_pred, self.config['metric_names'])
        evaluation_dict = evaluator_obj.evaluation_metrics_calculator()
        logger.write_to_logger('Make a set of evaluation metrics')

        # Sketch the anomaly plot
        plotter_obj = Plotter()
        anomaly_plot = plotter_obj.sensor_anomalies_plotter(df=trans_df, 
                                                            sensor_names=self.config['sensor_names'],
                                                            column_name='machine_status',
                                                            anomaly_method_name='IsolatedForest')
        
        # Sketch confusion matrix plot
        cm_plot = plotter_obj.cm_plotter(cm=evaluation_dict['confusion'], logarithm=False)

        # Sketch AUC-ROC curve
        auc_plot = plotter_obj.auc_roc_plotter(evaluation_dict['auc_roc'])

        # Save the plots in the output directory
        read_write_obj.plot_saver('image_directory', anomaly_plot, 'anomaly_plot.png')
        read_write_obj.plot_saver('image_directory', cm_plot, 'cm_plot.png')
        read_write_obj.plot_saver('image_directory', auc_plot, 'auc_roc_plot.png')
        logger.write_to_logger('saved all the Images')

        # Save the transformed dataframe
        read_write_obj.dataframe_writer('output_directory', trans_df, f'transformed_{file_name}')
        logger.write_to_logger(f'saved transformed datframe: {file_name}')

        # Save evaluation metrics
        read_write_obj.dictionary_saver('output_directory', evaluation_dict, 'evaluation.pickle')
        logger.write_to_logger('saved evaluation metrics')

        # Remove the raw file from target directory
        read_write_obj.file_remover('target_directory', file_name)
        logger.write_to_logger(f'removed raw dataframe: {file_name}')

if __name__ == "__main__":
    config = ConfigReader()
    target_directory = config['target_directory']
    watcher = DataDirectoryWatcher(target_directory, Main.main)
    watcher.start_watching()