import pandas as pd
from ConfigReader import ConfigReader
from ReadWriteClass import Reader, Writer

class DataDivider:
    config = ConfigReader()

    def __init__(self, df):
        self.df = self.index_changer(df)
    
    def index_changer(self, df):
        """
        this function changes the index from integer numbers to dates
        """
        # change the type of the timestamp column
        df['timestamp'] = pd.to_datetime(df['timestamp'])

        # set timestamp column as the index
        df.set_index('timestamp', inplace=True)

        return df

    def data_divider(self, division_range='M'):
        """
        this method divide the dataset into definite number of 
        training and testing datasets, then save them in a determined path
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
    reader_obj = Reader()
    writer_obj = Writer()

    # Read the row data
    df = reader_obj.dataframe_reader(raw_file_dir, file_name)

    # Divide the dataset
    data_divider_obj = DataDivider(df)
    df_dictionary = data_divider_obj.data_divider()

    # save the dataframes
    for name , dataframe in df_dictionary.items():
        writer_obj.dataframe_writer(divided_df_dir, dataframe, name)

if __name__ == '__main__':
    main('raw_file_directory', 'divided_data_directory', 'sensor.csv')