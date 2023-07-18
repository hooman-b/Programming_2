import json
import csv
import re
import pandas as pd
import linecache as lc
from exceptions import LenghtDiscripancy

class DataProvider:
    def __init__(self):

        self.property = 'value'
        self.file_path = "D:/Python/data_programming_2/week3_data/DSST.csv"
        self.keys = self.key_maker()

    def key_maker(self):
        csv_file = open(self.file_path)
        header = csv_file.readline()
        keys_string = header.strip("\n")
        keys_list = re.split(',', keys_string)
        csv_file.close()
        return keys_list

    # method should not start with a capital letter
    # also, this method has quite a few parameters, not all of which
    # will be necessary in all calls...
    def Get_data(self, get_all, single_year, year_low, year_high):

        result = self.get_json()
        df = pd.DataFrame.from_dict(result)

        if get_all:
            return df.to_json(orient='records')

        if single_year != "":
            df = df[df["Year"] == single_year]
    
            if len(df) > 0:
                return df.to_json(orient='records')
            
            else:
                raise Exception(f"There is no data for year {single_year}")

        if year_low != "" and year_high != "":
            df = df[(df["Year"] >= year_low) & (df["Year"] <= year_high)]

            if len(df) > 0:
                return df.to_json(orient='records')

            else:
                raise Exception(
                    f"There is no data between year {year_low} and {year_high}")

    def get_json(self):

        json_list = []

        line_number = 0

        while True:
            line_number += 1
            line = lc.getline(self.file_path, line_number)

            if not line:
                print("Data frame is finished.")
                break

            line = line.strip("\n")
            vals_list = re.split(',', line)
            assert len(vals_list) == len(self.keys) or \
                        LenghtDiscripancy(len(self.keys), len(vals_list))
            
            json_list.append(dict(zip(self.keys, vals_list)))

        return json_list

if __name__ == '__main__':
    dataProvider = DataProvider()
    dataProvider.Get_data(False, "2000", "", "")