import json
import os

class JsonFileFactory:
    def write_data(self, arr_data, filename):
        json_string = json.dumps([item.__dict__ for item in arr_data], indent=4, ensure_ascii=False)
        with open(filename, 'w', encoding='utf-8') as json_file:
            json_file.write(json_string)

    def read_data(self, filename, ClassName):
        if not os.path.isfile(filename):
            return []
        with open(filename, 'r', encoding='utf-8') as file:
            arr_data = json.loads(file.read(), object_hook=lambda cls: ClassName(**cls))
        return arr_data
