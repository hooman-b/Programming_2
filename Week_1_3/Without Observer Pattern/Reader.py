# pylint: disable=E1101
import linecache as lc
from CsvConverter import CsvConverter

class Reader():
    """
    Explanation: A class for reading and processing data from a file.
    """
    def __init__(self, stride_length, path):
        """
        Input: 1. stride_length (int): The number of lines to read at each iteration.
               2. path (str): The path to the data file.
        Explanation: Initializes a Reader instance.
        """
        self.path = path
        self.stride_length = stride_length
        self.read_lines = 2
        self.current_line = 2
        self.observer_list = []
        self.csv_converter = CsvConverter(lc.getline(self.path, 1))

    def get_lines(self):
        """
        Output: (str): A JSON formatted string containing the processed data.
        Explanation: Reads and processes the next set of lines from the file.
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
    directory = 'D:/Python/data_programming_2/dSST.csv'
    red = Reader(5, directory)
#    red.get_lines() #returns lines 2-6 as json
#    red.get_lines() #returns lines 7-11 as json
#    print(len(red.get_lines())) #returns lines 12-16 as json