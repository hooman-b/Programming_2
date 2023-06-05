import re
import json
from exceptions import LenghtDiscripancy

class CsvConverter():

    def __init__(self, csv_file):
        self.vals = self.vals_maker(csv_file)
        self.keys = self.key_maker(csv_file)

    def key_maker(self, csv_file):
        # asking teacher about using re library
        keys_string = csv_file[0]
        keys_list = re.split(',', keys_string)
        return keys_list

    def vals_maker(self, csv_file):
        vals_list = []
        for line in csv_file[1:]:
            vals_list.append(line)
        return vals_list

    def csv_to_json(self):
        json_list = []

        for line in self.vals:
            vals_list = re.split(',', line)
            assert len(vals_list) == len(self.keys), \
                    LenghtDiscripancy(len(self.keys), len(vals_list))
            json_list.append(dict(zip(self.keys, vals_list)))

        return json.dumps(json_list, indent=2)
