# pylint: disable=E1101
import pandas as pd
from Reader import Reader
from bbb import Animation

class AverageYear():
    def __init__(self, reader):
        self.reader = reader
        self.average_number = 1
    #    self.total_mean = self.year_temp_average_maker()

    #def __str__(self):
    #    return f'the total average value is {self.total_mean}'

    def temp_average_maker(self):

        # Ask how can you improve this structure
        while True:

        #    temp_list = []
            temp_df = pd.read_json(self.reader.get_lines())

            # Check if the DataFrame has at least 13 columns
            if temp_df.shape[1] == 0:
                print("DataFrame doesn't have enough columns.")
                break
            
            temp_average = temp_df.iloc[:, 1:13].mean(axis=None)
            year_average = temp_df.iloc[:, 0].mean(axis=0)
        #    temp_list.append(temp_average)
            yield year_average, [temp_average]

class AverageMonth():
    def __init__(self, reader):
        self.reader = reader
        self.average_number = 12
    #    self.monthly_mean = self.monthly_temp_average_maker()
    
    #def __str__(self):
    #    return f'the monthly average values are\n{self.monthly_mean}'

    def temp_average_maker(self):

        # Ask how can you improve this structure
        while True:

            temp_df = pd.read_json(self.reader.get_lines())

            # Check if the DataFrame has at least 13 columns
            if temp_df.shape[1] == 0:
                print("DataFrame doesn't have enough columns.")
                break

            temp_average = temp_df.iloc[:, 1:14].mean(axis=0)
            year_average = temp_df.iloc[:, 0].mean(axis=0)
            print(temp_average.index)
            yield year_average, temp_average

if __name__ == "__main__":
    reader_object = Reader(5)
    Average_year_object = AverageYear(reader_object)
    Animation(Average_year_object)

