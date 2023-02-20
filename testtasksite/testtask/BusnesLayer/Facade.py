import numpy as np

from .Mean import Mean
from .Gap import GapFormatter


class Facade:
    output_date_format: str = '%Y-%m-%dT%H:%M:%SZ'

    def __init__(self, json_data, mean_calculator: Mean):
        self.__json = json_data
        self.__mean_calculator = mean_calculator
        self.gap_generator = GapFormatter(json_data)
        self.__target = self.gap_generator.get_target()
        self.__mean_calculator.target = self.__target

    def calculate_means(self):
        gaps = self.gap_generator.generate()
        dataset = self.gap_generator.get_dataset()
        needed_time = self.gap_generator.get_datefrom().time()

        res_list = list()
        for gap in gaps[0::1]:
            self.__mean_calculator.data = dataset[gap.StartInd: gap.EndInd]
            date = gap.DateFrom.replace(hour=needed_time.hour, minute=needed_time.minute, second=needed_time.second)
            res_list.append({"date": date.strftime(self.output_date_format),
                             self.__target: self.__mean_calculator.compute()})

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
