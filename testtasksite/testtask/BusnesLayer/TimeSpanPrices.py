import json
from datetime import datetime


class TimeSpanPrices:
    __input_date_format: str = '%Y-%m-%dT%H:%M:%S.%fZ'
    __output_date_format: str = '%Y-%m-%dT%H:%M:%SZ'
    __compared_field: str = 'date'

    @classmethod
    def get_input_date_format(cls):
        return cls.__input_date_format

    @classmethod
    def get_output_date_format(cls):
        return cls.__output_date_format

    @classmethod
    def get_compared_field(cls):
        return cls.__compared_field



    @classmethod
    def from_file(cls, filename: str):
        with open(filename) as file:
            data = json.load(file)
        return cls(data)

    @classmethod
    def from_str(cls, json_str: str):
        return cls(json.loads(json_str))

    def __init__(self, json_data):
        self.__date_from = datetime.strptime(json_data['dateFrom'], self.__input_date_format)
        self.__date_to = datetime.strptime(json_data['dateTo'], self.__input_date_format)
        self.__target = json_data['target']
        self.__data = json_data['data']
        self.__dif_of_days = None

    def get_date_from(self):
        return self.__date_from

    def get_date_to(self):
        return self.__date_to

    def get_target(self):
        return self.__target

    def get_dataset(self):
        return self.__data

    def get_timespan_days(self):
        if self.__dif_of_days is None:
            self.__dif_of_days = (self.__date_to - self.__date_from).days
        return self.__dif_of_days