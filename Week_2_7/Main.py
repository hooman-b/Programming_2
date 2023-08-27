from ConfigReader import ConfigReader
from MyWatchdog import DataDirectoryWatcher
from ReadWriteClass import ReadWrite
from DataManager import DataManager
from ModelEvaluator import ModelEvaluator
from Model import Model
from Plotter import Plotter

# Assign config as a global variable
config = ConfigReader()

# Function to process the newly added data file
def main(file_name):
    """
    This is the main function of the program that implement all
    the process on a new observed dataset.
    """
    # Print the new file path
    print(f"Processing data from file: {file_name}")

    # make the dataframe
    read_write_obj = ReadWrite()
    raw_df = read_write_obj.dataframe_reader(config['target_directory'], file_name)

    # Transform the raw dataframe
    data_manager_obj = DataManager(raw_df,
                              fill_method='ffill',
                              smoothing_par=None,
                              smoothing_method='exponential',
                              norm_name='min_max')

    trans_df = data_manager_obj.dataframe_manager()

    # Call the trained model
    model = Model(config['model_directory'], 'if_model.joblib')

    # Predict the new labels
    y_pred = model.predict(trans_df.iloc[:, :-1])

    # Save the predicted column in the transform dataframe
    trans_df['IsolatedForest'] = y_pred

    # Make a dictionary of evaluation metrics
    evaluator_obj = ModelEvaluator(trans_df['machine_status'], y_pred, config['metric_names'])
    evaluation_dict = evaluator_obj.evaluation_metrics_calculator()

    # Sketch the anomaly plot
    plotter_obj = Plotter()
    anomaly_plot = plotter_obj.sensor_anomalies_plotter(df=trans_df, 
                                                        sensor_names=config['sensor_names'],
                                                        column_name='machine_status',
                                                        anomaly_method_name='IsolatedForest')
    
    # Sketch confusion matrix plot
    cm_plot = plotter_obj.cm_plotter(cm=evaluation_dict['confusion_matrix'], logarithm=False)

    # Sketch AUC-ROC curve
    auc_plot = plotter_obj.auc_roc_plotter(evaluation_dict['auc_roc'])

    # Save the plots in the output directory
    read_write_obj.plot_saver('output_directory', anomaly_plot, 'anomaly_plot.jpg')
    read_write_obj.plot_saver('output_directory', cm_plot, 'cm_plot.jpg')
    read_write_obj.plot_saver('output_directory', auc_plot, 'auc_roc_plot.jpg')

    # Save the transformed dataframe
    read_write_obj.dataframe_writer('output_directory', trans_df, f'transformed_{file_name}')

    # Save evaluation metrics
     read_write_obj.dictionary_saver('output_directory', evaluation_dict, 'evaluation.txt')

    # Remove the raw file from target directory
    read_write_obj.file_remover('target_directory', file_name)

if __name__ == "__main__":

    target_directory = config['target_directory']
    watcher = DataDirectoryWatcher(target_directory, main)
    watcher.start_watching()