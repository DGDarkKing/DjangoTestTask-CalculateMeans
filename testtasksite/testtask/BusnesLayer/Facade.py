import numpy as np

from .TimeSpanPrices import TimeSpanPrices
from .Mean import Mean
from .Gap import GapGenerator


class Facade:

    def __init__(self, timespan_prices: TimeSpanPrices, mean_calculator: Mean):
        self.__timespan_prices = timespan_prices
        self.__target = self.__timespan_prices.get_target()
        self.gap_generator = GapGenerator(timespan_prices)
        self.__mean_calculator = mean_calculator
        self.__mean_calculator.target = self.__target

    def calculate_means(self):
        gaps = self.gap_generator.generate()

        result_list = list()
        dataset = self.__timespan_prices.get_dataset()
        needed_time = self.__timespan_prices.get_date_from().time()
        output_date_format = self.__timespan_prices.get_output_date_format()
        for gap in gaps[0::1]:
            self.__mean_calculator.data = dataset[gap.StartInd: gap.EndInd]
            output_date = gap.DateFrom.replace(hour=needed_time.hour, minute=needed_time.minute, second=needed_time.second)
            result_list.append({"date": output_date.strftime(output_date_format),
                                self.__target: self.__mean_calculator.compute()})

        self.__post_processing(result_list)
        return result_list



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
