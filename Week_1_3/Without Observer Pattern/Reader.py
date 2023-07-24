# pylint: disable=E1101
import time
import pandas as pd
import linecache as lc
from CsvConverter import CsvConverter

class Reader():

    def __init__(self, line_number, path='dSST.csv'):
        self.path = path
        # I think the name of this field is wrong. Shouldn't it be something like `stride_length`?`
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


if __name__ == "__main__":

    
    red = Reader(5)
#    red.get_lines() #returns lines 2-6 as json
#    red.get_lines() #returns lines 7-11 as json
#    print(len(red.get_lines())) #returns lines 12-16 as json