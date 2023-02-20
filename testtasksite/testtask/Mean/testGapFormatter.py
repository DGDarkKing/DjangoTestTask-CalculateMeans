

import json
from datetime import datetime, timedelta
from typing import Any

from .Gap import Gap


class GapFormatter:
    __dateFormat: str = '%Y-%m-%dT%H:%M:%S.%fZ'

    @classmethod
    def from_file(cls, filename: str):
        with open(filename) as file:
            data = json.load(file)
        return cls(data)

    @classmethod
    def from_str(cls, jsonstr: str):
        data = json.load(jsonstr)
        return cls(data)

    def __init__(self, jsondata):
        self.__json = jsondata

        self.__target = self.__json['target']
        self.__data = self.__json['data']

        self.__dateFrom = datetime.strptime(self.__json['dateFrom'], self.__dateFormat)

        self.__dateTo = datetime.strptime(self.__json['dateTo'], self.__dateFormat)
        self.__dateTo = datetime(year=self.__dateTo.year, month=self.__dateTo.month, day=self.__dateTo.day,
                                 hour=23, minute=59, second=59)

    def generate(self, gaps: list):
        dif_from_to_days = (self.__dateTo - self.__dateFrom).days
        deltatime_gap = self.__definition_timeinterval(dif_from_to_days)
        cur_gap_start = self.__dateFrom
        cur_gap_end = cur_gap_start + deltatime_gap

        find = self.__find(cur_gap_end.strftime(self.__dateFormat), deltatime_gap)
        start_ind = 0
        for ind in find:
            if ind == -1:
                gaps.append(Gap(date_from=cur_gap_start, date_end=cur_gap_end))
            else:
                gaps.append(Gap(date_from=cur_gap_start, date_end=cur_gap_end, start_ind=start_ind, end_ind=ind+1))
                start_ind = ind+1
            cur_gap_start = cur_gap_end
            cur_gap_end = cur_gap_start + deltatime_gap
            find.send(cur_gap_end.strftime(self.__dateFormat))

    def get_dataset(self):
        return self.__data

    def get_target(self):
        return self.__target

    def get_datefrom(self):
        return self.__dateFrom

    def get_dateto(self):
        return self.__dateTo



    def __definition_timeinterval(self, days: int):
        if days > 366:
            return timedelta(weeks=2)
        elif days > 31:
            return timedelta(weeks=1)
        else:
            return timedelta(days=1)

    # !!! ATTENTION !!!
    # Function has 4 operator YIELD (Two in a row)
    #   first YIELD returns data and setting new value by using method send of Generator
    #   second YIELD returns immediately after setting new data
    def __find(self, x: str, delta: timedelta):
        start_ind = 0
        length = len(self.__data)
        mid = (length - start_ind) // 2
        while start_ind < length:
            mid_date = self.__data[mid + start_ind]['date']
            if x <= mid_date:
                if mid == 0:
                    while mid == 0:
                        x = yield -1 # !!! First pair of YIELD - nothing found
                        yield
                        if x > self.__data[start_ind]['date']: # If
                            mid = 1

                    mid = (length - start_ind) // 2
                else:
                    mid = mid // 2
            else:
                result = start_ind + mid
                while x > mid_date:
                    result += 1
                    if(result >= length):
                        result -= 1
                        break
                    mid_date = self.__data[result]['date']

                if x <= mid_date:
                    result -= 1
                mid = result - start_ind
                x = yield result # Second pair of YIELD
                yield
                start_ind = start_ind + mid+1
                mid = (length - start_ind) // 2
