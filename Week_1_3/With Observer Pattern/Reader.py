# pylint: disable=E1101
import pandas as pd
import linecache as lc
from Subject import Subject
from CsvConverter import CsvConverter
from ConsumingClasses import AverageYear, AverageMonth
from Animation import Animation

# Nice to use inheritance in this case.
class Reader(Subject):
    """
    Explanation: A class for reading and processing CSV data in chunks using observers.
    """

    def __init__(self, stride_length, path):
        """
        Input: 1. stride_length (int): The number of lines to read in each iteration.
               2. path (str): The path to the CSV file.
        Explanation: Initializes a Reader instance with necessary attributes.
        """
        Subject.__init__(self)
        self.path = path
        self.stride_length = stride_length
        self.read_lines = 2
        self.current_line = 2
        self.observer_list = []
        self.csv_converter = CsvConverter(lc.getline(self.path, 1))

    def __iter__(self):
        """
        Explanation: Returns the Reader instance as an iterator.
        """
        return self

    def __next__(self):
        """
        Explanation: Reads and processes the next chunk of data.
        Output: 1. (pd.DataFrame): The processed data in a DataFrame.
        """
        json_file = self.get_lines()
        temp_df = pd.read_json(json_file)

        if temp_df.shape[1] == 0:
            print("DataFrame doesn't have enough columns.")
            self.notify_observers(temp_df)
            raise StopIteration

        self.notify_observers(temp_df)

    def get_lines(self):
        """
        Explanation: Reads lines from the CSV file and converts them to JSON.
        Output: 1.  (str): The JSON-formatted data.
        """
        lines_list = []
        print(self.current_line)

        for line_number in range(self.stride_length):      
            lines_list.append(lc.getline(self.path, self.current_line + line_number))

        json_file = self.csv_converter.csv_to_json(lines_list)
        self.current_line += self.stride_length
        self.read_lines = self.current_line
        return json_file

if __name__ == "__main__":
    directory = 'D:\\Python\\data_programming_2\\week3_data\\dSST.csv'
    reader = Reader(5, directory)

    average_year = AverageYear()
    animation_year = Animation(1)

    average_month = AverageMonth()
    animation_month = Animation(12)
    
    # Connect Reader to the first layer observers
    reader.add_observer(average_year)
    reader.add_observer(average_month)

    # Connect the first layer observers to the second layer
    average_year.add_observer(animation_year)
    average_month.add_observer(animation_month)

    # Start the data iteration using a for loop
    for data_frame in reader:
        pass

