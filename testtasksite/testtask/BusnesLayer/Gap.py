
import json
from datetime import timedelta

from datetime import datetime

from .TimeSpanPrices import TimeSpanPrices


class Gap:
    __dateFormat: str = '%Y-%m-%dT%H:%M:%S.%fZ'

    def __init__(self, date_from: datetime, date_end: datetime, start_ind: int = -1, end_ind: int = -1):
        self.DateFrom = date_from
        self.DateTo = date_end
        self.StartInd = start_ind
        self.EndInd = end_ind

    def __str__(self):
        return f'"DateFrom": {self.DateFrom.strftime(Gap.__dateFormat)},\n' \
               f'"DateTo": {self.DateTo.strftime(Gap.__dateFormat)}\n' \
               f'"StartInd": {self.StartInd}\n' \
               f'"EndIndex": {self.EndInd}'




class GapGenerator:

    def __init__(self, timespan_prices: TimeSpanPrices):
        self.__timespan_prices = timespan_prices
        self.__date_format = timespan_prices.get_input_date_format()
        self.__data = timespan_prices.get_dataset()
        self.__compared_field = timespan_prices.get_compared_field()

    def generate(self):
        gaps = list()
        gap_delta_days = self.__definition_timeinterval(self.__timespan_prices.get_timespan_days())
        current_date_start = self.__timespan_prices.get_date_from().replace(hour=0, minute=0, second=0)
        current_date_end = current_date_start + gap_delta_days

        find = self.__find(current_date_end.strftime(self.__date_format), gap_delta_days)
        start_ind = 0
        for ind in find:
            if ind == -1:
                gaps.append(Gap(date_from=current_date_start, date_end=current_date_end))
            else:
                gaps.append(Gap(date_from=current_date_start, date_end=current_date_end, start_ind=start_ind, end_ind=ind +1))
                start_ind = ind + 1
            current_date_start = current_date_end
            current_date_end = current_date_start + gap_delta_days
            find.send(current_date_end.strftime(self.__date_format))

        return gaps

    def __definition_timeinterval(self, days: int):
        if days > 366:
            return timedelta(weeks=2)
        elif days > 31:
            return timedelta(weeks=1)
        else:
            return timedelta(days=1)

    # !!! ATTENTION !!!
    # Function has 6 operator YIELD (Two in a row)
    #   first YIELD returns data and setting new value by using method send of Generator
    #   second YIELD returns immediately after setting new data
    #   third pair follows after second pair - check the first element in the new sequence
    def __find(self, x: str, delta: timedelta):
        start_index = 0
        LENGTH = len(self.__data)
        mid_index = (LENGTH - start_index) // 2
        while start_index < LENGTH:
            mid_date = self.__data[mid_index + start_index][self.__compared_field]
            if x <= mid_date:
                if mid_index == 0:
                    while mid_index == 0:
                        x = yield -1 # !!! First pair of YIELD - nothing found
                        yield
                        if x > self.__data[start_index][self.__compared_field]:
                            mid_index = 1

                    mid_index = (LENGTH - start_index) // 2
                else:
                    mid_index = mid_index // 2
            else:
                result_index = start_index + mid_index
                while x > mid_date:
                    result_index += 1
                    if(result_index >= LENGTH):
                        result_index -= 1
                        break
                    mid_date = self.__data[result_index][self.__compared_field]

                if x <= mid_date:
                    result_index -= 1
                mid_index = result_index - start_index
                x = yield result_index # Second pair of YIELD
                yield
                start_index = start_index + mid_index + 1
                if start_index < LENGTH:
                    while x <= self.__data[start_index][self.__compared_field]:
                        x = yield -1  # !!! First pair of YIELD - nothing found
                        yield
                mid_index = (LENGTH - start_index) // 2
