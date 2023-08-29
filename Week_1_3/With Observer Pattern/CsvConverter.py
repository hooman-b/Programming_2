# pylint: disable=E0611
import json
from exceptions import LenghtDiscripancy

class CsvConverter():
    """
    Explanation: A class for converting CSV lines to JSON format using a
                 given header.
    """

    def __init__(self, header):
        """
        Input: 1. header (str): The CSV header line containing column names.
        Explanation: Initializes a CsvConverter instance with a given header.
        """
        self.keys = self.key_maker(header)
        print(header)

    def key_maker(self, header):
        """
        Input: 1.  header (str): The CSV header line containing column names.
        Explanation: Creates a list of keys (column names) from a given header.
        Output: 1. list: A list of keys extracted from the header.
        """
        keys_string = header.strip("\n")
        keys_list = keys_string.split(',')
        return keys_list

    def csv_to_json(self, csv_lines):
        """
        Input: 1.  csv_lines (list): A list of CSV lines to be converted.
        Explanation: Converts a list of CSV lines into a JSON-formatted string.
        Output: 1. str: A JSON-formatted string representing the converted data.
        """
        json_list = []

        # modify and add each line to the json list
        for line in csv_lines:
            line = line.strip("\n")
            vals_list = line.split(',')

            if len(vals_list) != 1:
                assert len(vals_list) == len(self.keys) or \
                        LenghtDiscripancy(len(self.keys), len(vals_list))

                json_list.append(dict(zip(self.keys, vals_list)))

        return json.dumps(json_list, indent=2)
