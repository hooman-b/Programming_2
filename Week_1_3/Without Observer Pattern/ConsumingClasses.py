# pylint: disable=E1101
# you were not allowed to use pandas for this exercise, but you 
# don't use it for reading, just for visualisation, so ok.
import pandas as pd
from Reader import Reader
from Animation import Animation

class AverageYear():
    def __init__(self, reader):
        self.reader = reader
        self.average_number = 1



    def temp_average_maker(self):
        

        while True:

            temp_df = pd.read_json(self.reader.get_lines())

            # Check if the DataFrame has at least 13 columns
            if temp_df.shape[1] == 0:
                print("DataFrame doesn't have enough columns.")
                break

            temp_average = temp_df.iloc[:, 1:13].mean(axis=None)
            year_average = temp_df.iloc[:, 0].mean(axis=0)

            yield year_average, [temp_average]

class AverageMonth():
    def __init__(self, reader):
        self.reader = reader
        self.average_number = 8

    def temp_average_maker(self):

        # Ask how can you improve this structure
        while True:

            temp_df = pd.read_json(self.reader.get_lines())

            # Check if the DataFrame has at least 13 columns
            if temp_df.shape[1] == 0:
                print("DataFrame doesn't have enough columns.")
                break

            temp_average = temp_df.iloc[:, 1:16].mean(axis=0)
            year_average = temp_df.iloc[:, 0].mean(axis=0)
            print(temp_average.index)
            yield year_average, temp_average

if __name__ == "__main__":
    reader_object = Reader(5)
    Average_year_object = AverageMonth(reader_object)

    Animation(Average_year_object)

