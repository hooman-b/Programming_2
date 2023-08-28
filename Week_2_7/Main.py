# pylint: disable=E1101
import time
from ConfigReader import ConfigReader
from MyWatchdog import DataDirectoryWatcher
from ReadWriteClass import Reader, Writer
from DataManager import DataManager
from ModelEvaluator import ModelEvaluator
from Model import Model
from Plotter import Plotter
from Logger import log

config = ConfigReader()

class Main():
    """
    Type: The Main class to process new data files and perform various tasks.
    Explanation: This class defines the main processing flow for a new observed dataset.
                 It loads, transforms, predicts, evaluates, and saves data using various
                 classes and modules.
    """
    # Function to process the newly added data file
    def main(self, file_name):
        """
        Input: 1. file_name (str): The name of the new data file.
        Explanation: Process a newly added data file.
        """
        try:
            time.sleep(10)
            # make logging 
            logger_obj = log('main_program.log')

            #matplotlib.use('agg')
            reader_obj = Reader(logger_obj)
            writer_obj = Writer(logger_obj)

            # Print the new file path
            print(f'Found new data file: {file_name}')
            logger_obj.write_to_logger(f'Found new data file: {file_name}')

            # make the dataframe
            raw_df = reader_obj.dataframe_reader('target_directory', file_name)
            logger_obj.write_to_logger('Loaded the file')

            # Transform the raw dataframe
            data_manager_obj = DataManager(raw_df,
                                smoothing_par=None,
                                smoothing_method='exponential',
                                norm_name='min_max',
                                fe_switch=False)

            trans_df = data_manager_obj.dataframe_manager()
            logger_obj.write_to_logger('Received transformed data')

            # Call the trained model
            model = Model('model_directory', 'if_model.joblib', logger_obj)

            # Predict the new labels
            y_pred = model.predict(trans_df.iloc[:, :-1])
            logger_obj.write_to_logger('Received predicions')

            # Save the predicted column in the transform dataframe
            trans_df['IsolatedForest'] = y_pred
            logger_obj.write_to_logger('Add predicions to the dataset')

            # Make a dictionary of evaluation metrics
            evaluator_obj = ModelEvaluator(trans_df['machine_status'], y_pred, config['metric_names'])
            evaluation_dict = evaluator_obj.evaluation_metrics_calculator()
            logger_obj.write_to_logger('Make a set of evaluation metrics')

            # Sketch the anomaly plot
            plotter_obj = Plotter()
            anomaly_plot = plotter_obj.sensor_anomalies_plotter(df=trans_df,
                                                                sensor_names=config['sensor_names'],
                                                                column_name='machine_status',
                                                                anomaly_method_name='IsolatedForest')

            # Sketch confusion matrix plot
            cm_plot = plotter_obj.cm_plotter(cm=evaluation_dict['confusion'], logarithm=False)

            # Sketch AUC-ROC curve
            auc_plot = plotter_obj.auc_roc_plotter(evaluation_dict['auc_roc'])

            # Save the plots in the output directory
            df_date = trans_df.index.dt.to_period('M')
            writer_obj.plot_writer('image_directory', anomaly_plot, f'{df_date[0]}_anomaly_plot.png')
            logger_obj.write_to_logger('saved anomaly_plot.png')

            writer_obj.plot_writer('image_directory', cm_plot, 'cm_plot.png')
            logger_obj.write_to_logger('saved cm_plot.png')

            writer_obj.plot_writer('image_directory', auc_plot, 'auc_roc_plot.png')
            logger_obj.write_to_logger('saved auc_roc_plot.png')

            # Save the transformed dataframe
            writer_obj.dataframe_writer('output_directory', trans_df, f'transformed_{file_name}')
            logger_obj.write_to_logger(f'saved transformed datframe: transformed_{file_name}')

            # Save evaluation metrics
            writer_obj.dictionary_writer('output_directory', evaluation_dict, 'evaluation.pickle')
            logger_obj.write_to_logger('saved evaluation metrics')

            # Remove the raw file from target directory
            writer_obj.file_remover('target_directory', file_name)
            logger_obj.write_to_logger(f'removed raw dataframe: {file_name}')

        except ValueError as error:
            logger_obj.error_to_logger(f"Value error: {str(error)}")
            print(f"Value error: {str(error)}")

        except KeyError as error:
            logger_obj.error_to_logger(f"Key error: {str(error)}")
            print(f"Key error: {str(error)}")

        finally:
            print('precess has finished')

if __name__ == "__main__":
    target_directory = config['target_directory']
    watcher = DataDirectoryWatcher(target_directory, Main.main)
    watcher.start_watching()