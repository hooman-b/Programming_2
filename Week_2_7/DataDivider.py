import pandas as pd
from ConfigReader import ConfigReader
from ReadWriteClass import Reader, Writer
from Logger import log

class DataDivider:
    """
    Type: A class for dividing a DataFrame into training and testing datasets.
    Explanation: This class provides methods to change the index of the DataFrame to dates
                 and divide it into a training dataset and multiple testing datasets.   
    Attributes: df (pandas.DataFrame): The DataFrame to be divided.

    """
    config = ConfigReader()

    def __init__(self, df):
        """
        Input: df (pandas.DataFrame): The DataFrame to be divided.
        Explanation: Initialize the DataDivider object.
        """
        self.df = self.index_changer(df)
    
    def index_changer(self, df):
        """
        Input: df (pandas.DataFrame): The DataFrame to have its index changed.
        Explanation: Change the index of the DataFrame from integer numbers to dates.
        Output: (pandas.DataFrame) The DataFrame with the changed index.
        """
        # change the type of the timestamp column
        df['timestamp'] = pd.to_datetime(df['timestamp'])

        # set timestamp column as the index
        df.set_index('timestamp', inplace=True)

        return df

    def data_divider(self, division_range='M'):
        """
        Input: division_range (str): The frequency of division (e.g., 'M' for monthly).
        Explanation: Divide the dataset into training and testing datasets.        
        Output: 1. (dict) A dictionary containing the divided DataFrames.
        """
        df_dict = {}
        # Make a series of the range in which wants to divide the data
        start_date = self.df.index.min()
        end_date = self.df.index.max()
        dates = pd.date_range(start=start_date, end=end_date, freq=division_range)

        # Slice around 60% of the dataset for training purpose
        train_month_number = int(len(dates) * 0.6) - 1
        df_train = self.df.loc[:dates[train_month_number]]

        # add the train dataset
        df_dict['df_train.csv'] = df_train

        # add all the test sets
        for number, counter in enumerate(range(train_month_number, len(dates) - 1, 1)):
            df_test = self.df.loc[dates[counter]:dates[counter+1]]
            df_dict[f'df_test{number+1}.csv'] = df_test

        return df_dict

def main(raw_file_dir, divided_df_dir, file_name):
    """
    Input: 1. raw_file_dir (str): The directory containing the raw data file.
           2. divided_df_dir (str): The directory to save the divided datasets.
           3. file_name (str): The name of the raw data file.
    Explanation: The main function for dividing a dataset into training and testing datasets.
    """
    logger_obj = log('data_divider.log')
    reader_obj = Reader(logger_obj)
    writer_obj = Writer(logger_obj)

    # Read the row data
    df = reader_obj.dataframe_reader(raw_file_dir, file_name)
    logger_obj.write_to_logger('Loaded the raw file')

    # Divide the dataset
    data_divider_obj = DataDivider(df)
    df_dictionary = data_divider_obj.data_divider()
    logger_obj.write_to_logger('Received divided data dictionary')

    # Save the dataframes
    for name, dataframe in df_dictionary.items():
        writer_obj.dataframe_writer(divided_df_dir, dataframe, name)

    logger_obj.write_to_logger('Saved divided dataframes')

if __name__ == '__main__':
    main('raw_file_directory', 'divided_data_directory', 'sensor.csv')