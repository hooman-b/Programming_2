import yaml
import os
import pandas as pd

class DataDivider():

    def __init__(self, input_path):
        self.config = self.config_reader(input_path)
        self.df = self.dataframe_maker()

    def config_reader(self, input_path):
        """
        explanation: This function open config,yaml file 
        and fetch the gonfigue file information
        input: ...
        output: configue file
        """
        with open(input_path, "r", encoding="utf8") as input_file:
            config = yaml.safe_load(input_file)

        return config

    def dataframe_maker(self):
        """
        make the main dataset based on the configuration file
        """
        # make the dataframe
        file_directory, file_name, _ = self.config.values()
        os.chdir(file_directory)
        df = pd.read_csv(file_name).drop('Unnamed: 0', axis=1)

        # change the type of the timestamp column
        df['timestamp'] = pd.to_datetime(df['timestamp'])

        # set timestamp column as the index
        df.set_index('timestamp', inplace=True)

        return df

    def dataframe_divider(self, division_range='M'):
        """
        this method divide the dataset into definite number of 
        training and testing datasets, then save them in a determined path
        """
        # change the directory
        output_dir = self.config['output_path']
        os.makedirs(output_dir, exist_ok=True)

        # Make a series of the range in which wants to divide the data
        start_date = self.df.index.min()
        end_date = self.df.index.max()
        dates = pd.date_range(start=start_date, end=end_date, freq=division_range)

        # Slice around 60% of the dataset for training purpose
        train_month_number = int(len(dates) * 0.6) - 1
        df_train = self.df.loc[:dates[train_month_number]]

        # save the train dataset
        df_train.to_csv(os.path.join(output_dir, 'df_train.csv'))

        # save all the test sets
        for number, counter in enumerate(range(train_month_number, len(dates) - 1, 1)):
            df_test = self.df.loc[dates[counter]:dates[counter+1]]
            df_test.to_csv(os.path.join(output_dir, f'df_test{number+1}.csv'))

if __name__ == '__main__':

    # run the DataDivider class
    divider = DataDivider('config.yaml')
    divider.dataframe_divider()
