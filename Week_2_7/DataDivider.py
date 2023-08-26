import pandas as pd
from ConfigReader import ConfigReader
from ReadWriteClass import ReadWrite

class DataFrameMaker:
    config = ConfigReader()
    read_write_obj = ReadWrite()

    def dataframe_maker(self):
        """
        make the main dataset based on the configuration file
        """
        # make the dataframe
        df = self.read_write_obj.dataframe_reader('file_direction', 'file_name')
        df.drop('Unnamed: 0', axis=1)

        # change the type of the timestamp column
        df['timestamp'] = pd.to_datetime(df['timestamp'])

        # set timestamp column as the index
        df.set_index('timestamp', inplace=True)
        return df

class DataDivider:
    config = ConfigReader()
    read_write_obj = ReadWrite()

    def __init__(self, df):
        self.df = df

    def data_divider(self, division_range='M'):
        """
        this method divide the dataset into definite number of 
        training and testing datasets, then save them in a determined path
        """

        # Make a series of the range in which wants to divide the data
        start_date = self.df.index.min()
        end_date = self.df.index.max()
        dates = pd.date_range(start=start_date, end=end_date, freq=division_range)

        # Slice around 60% of the dataset for training purpose
        train_month_number = int(len(dates) * 0.6) - 1
        df_train = self.df.loc[:dates[train_month_number]]

        # save the train dataset
        self.read_write_obj.dataframe_writer(df_train, 'df_train.csv')

        # save all the test sets
        for number, counter in enumerate(range(train_month_number, len(dates) - 1, 1)):
            df_test = self.df.loc[dates[counter]:dates[counter+1]]
            self.read_write_obj.dataframe_writer(df_test, f'df_test{number+1}.csv')

if __name__ == '__main__':

    dataframe_builder = DataFrameMaker()
    df = dataframe_builder.dataframe_maker()

    data_divider = DataDivider(df)
    data_divider.data_divider()