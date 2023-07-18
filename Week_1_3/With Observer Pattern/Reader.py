# pylint: disable=E1101
import time
import pandas as pd
import linecache as lc
from Subject import Subject
from CsvConverter import CsvConverter
from ConsumingClasses import AverageYear, AverageMonth
from Animation import Animation

# Nice to use inheritance in this case.
class Reader(Subject):

    def __init__(self, line_number, path='D:\\Python\\data_programming_2\\week3_data\\dSST.csv'):
        Subject.__init__(self)
        self.path = path
        self.line_number = line_number
        self.read_lines = 2
        self.current_line = 2
        self.observer_list = []
        self.csv_converter = CsvConverter(lc.getline(self.path, 1))

    def get_lines(self):
        lines_list = []
        print(self.current_line)

        for line_number in range(self.line_number):      
            lines_list.append(lc.getline(self.path, self.current_line + line_number))

        json_file = self.csv_converter.csv_to_json(lines_list)
        self.current_line += self.line_number
        self.read_lines = self.current_line

        return json_file

    # Why not use the __iter__ method?
    def iterator(self):
        while True:
            json_file = self.get_lines()
            temp_df = pd.read_json(json_file)

            if temp_df.shape[1] == 0:
                print("DataFrame doesn't have enough columns.")
                self.notify_observers(temp_df)
                break

            self.notify_observers(temp_df)


if __name__ == "__main__":
    reader = Reader(5)

    average_year = AverageYear()
    animation_year = Animation(1)

    average_month = AverageMonth()
    animation_month = Animation(12)
    
    # Connect Reader and AverageYear
    reader.add_observer(average_year)
    reader.add_observer(average_month)

    # Connect AverageYear and Animation
    average_year.add_observer(animation_year)
    average_month.add_observer(animation_month)
    # Start the data iteration
    reader.iterator()

