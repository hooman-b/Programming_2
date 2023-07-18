import re
import json
from exceptions import LenghtDiscripancy

class CsvConverter():

    def __init__(self, header):
        self.keys = self.key_maker(header)
        print(header)

    def key_maker(self, header):
        keys_string = header.strip("\n")
        keys_list = re.split(',', keys_string)
        return keys_list

    def csv_to_json(self, csv_lines):
        json_list = []

        for line in csv_lines:
            line = line.strip("\n")
            # no need to use a regex if you just split on a simple string.
            # think about performance...
            vals_list = re.split(',', line)

            if len(vals_list) != 1:
                assert len(vals_list) == len(self.keys) or \
                        LenghtDiscripancy(len(self.keys), len(vals_list))

                json_list.append(dict(zip(self.keys, vals_list)))


        return json.dumps(json_list, indent=2)
