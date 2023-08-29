# pylint: disable=E0611
import re
import pandas as pd
import linecache as lc
from exceptions import LenghtDiscripancy

class DataProvider:
    """
    Type: A class responsible for providing weather data based on query parameters.
    Explanation: This class reads weather data from a CSV file and allows querying
    based on various criteria, including all data, a specific year, or a range of years.
    """
    def __init__(self):
        """
        Explanation: Initialize the DataProvider with properties and file path.
        """
        self.property = 'value'
        self.file_path = "D:/Python/data_programming_2/week3_data/DSST.csv"
        self.keys = self.key_maker()

    def key_maker(self):
        """
        Explanation: Extracts keys from the header of the CSV file.
        Output: (list): A list of keys extracted from the CSV header.
        """
        with open(self.file_path, 'r') as csv_file:
            header = csv_file.readline()
            keys_string = header.strip("\n")
            keys_list = re.split(',', keys_string)

        return keys_list

    def get_data(self, query_params):
        """
        Input: query_params (dict): A dictionary containing query parameters.
        Explanation: Retrieves data based on the provided query parameters.        
        Output: (str): JSON-formatted data based on the query parameters.
        """
        # Retrieve raw data in dictionary format
        result = self.get_json()
        df = pd.DataFrame.from_dict(result)

        # Check if query_params indicates getting all data
        if query_params["get_all"]:
            return df.to_json(orient='records')

        # Extract query parameters from the dictionary
        single_year = query_params["single_year"]
        year_low = query_params["year_low"]
        year_high = query_params["year_high"]

        # If single_year is provided, filter DataFrame by year
        if single_year:
            df = df[df["Year"] == single_year]

            if not df.empty:
                return df.to_json(orient='records')
            else:
                raise ValueError(f"There is no data for year {single_year}")

        # If year_low and year_high are provided, filter DataFrame by range of years
        if year_low and year_high:
            df = df[(df["Year"] >= year_low) & (df["Year"] <= year_high)]

            if not df.empty:
                return df.to_json(orient='records')
            else:
                raise ValueError(f"There is no data between year {year_low} and {year_high}")

    def get_json(self):
        """
        Explanation: Reads the CSV file and converts each line to a dictionary.
        Output: (list): A list of dictionaries, each representing a line of data from the CSV.
        """
        json_list = []
        line_number = 0

        # Iterate through each line in the CSV file
        while True:
            line_number += 1
            line = lc.getline(self.file_path, line_number)

            # Break the loop if there are no more lines to read
            if not line:
                print("Data frame is finished.")
                break

            # Remove newline character and split the line into values
            line = line.strip("\n")
            vals_list = re.split(',', line)
            
            # Check if the number of values matches the number of keys
            if len(vals_list) != len(self.keys):
                raise LenghtDiscripancy(len(self.keys), len(vals_list))

            # Convert the values into a dictionary using keys and append to the list
            json_list.append(dict(zip(self.keys, vals_list)))

        return json_list

if __name__ == '__main__':
    dataProvider = DataProvider()
    query_params = {
        "get_all": False,
        "single_year": "2000",
        "year_low": "",
        "year_high": ""
    }

    dataProvider.get_data(query_params)