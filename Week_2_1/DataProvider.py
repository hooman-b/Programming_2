import json
import pandas as pd


class DataProvider:
    def __init__(self):
        self.property = 'value'
        self.file_path = "DSST.csv"
        csv_file = open(self.file_path)
        line_header = csv_file.readline()
        self.line_header = str.split(line_header, ',')

    def GetData(self, getAll, single_year, year_low, year_high):
        result = self.get_json()

        result = str.replace(result, "\n", "")
        result = str.replace(result, " ", "")
        result = str.replace(result, "},]", "}]")
        jsonVal = json.loads(result)
        df = pd.DataFrame.from_dict(jsonVal)
        if getAll:
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
        csv_file = open(self.file_path, 'r')
        line_number = -1
        json_value = "["
        while True:
            line = csv_file.readline()
            line_number += 1
            if not line:
                break
            line_value = line.split(',')
            if line_number == 0:
                continue
            assert len(line_value) == len(
                self.line_header), f"line {line_number}'s length does not match with header"
            json_value += "{"
            for index, key in enumerate(self.line_header):
                json_value += "\"" + \
                    self.line_header[index] + "\": \"" + \
                    line_value[index] + "\","
            json_value += "},"
            json_value = str.replace(json_value, ",},", "},")
        json_value += "]"
        csv_file.close()
        return json_value
