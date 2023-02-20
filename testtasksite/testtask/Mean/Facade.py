import numpy as np

from .Mean import Mean
from .testGapFormatter import GapFormatter


class Facade:

    def __init__(self, json_data, meaner):
        self.output_date_format = '%Y-%m-%dT%H:%M:%SZ'
        self.__json = json_data
        self.__meaner = meaner
        self.__target = ''
        pass

    def run(self):
        gap_generator = GapFormatter(self.__json)
        gaps = list()
        gap_generator.generate(gaps)

        dataset = gap_generator.get_dataset()
        self.__target = gap_generator.get_target()
        self.__meaner.target = self.__target
        needed_time = gap_generator.get_datefrom().time()

        res_list = list()
        for gap in gaps[0::1]:
            self.__meaner.data = dataset[gap.StartInd: gap.EndInd]
            date = gap.DateFrom.replace(hour=needed_time.hour, minute=needed_time.minute, second=needed_time.second)
            res_list.append({"date": date.strftime(self.output_date_format), self.__target: self.__meaner.compute()})

        self.__post_processing(res_list)
        return res_list

    def __post_processing(self, data_list):
        i = 0
        if np.isnan(data_list[i][self.__target]):
            while np.isnan(data_list[i][self.__target]):
                i += 1
            substitute = int(data_list[i][self.__target])
            i = 0
            while np.isnan(data_list[i][self.__target]):
                data_list[i][self.__target] = substitute
                i += 1

        while i < len(data_list):
            if np.isnan(data_list[i][self.__target]):
                data_list[i][self.__target] = data_list[i - 1][self.__target]
            else:
                data_list[i][self.__target] = int(data_list[i][self.__target])
            i += 1
