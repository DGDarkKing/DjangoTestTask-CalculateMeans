from functools import reduce
from math import sqrt
import numpy as np

from .Mean import Mean


class MyMean(Mean):

    def __init__(self, target=None, data=None):
        super(MyMean, self).__init__(target, data)

    def compute(self):
        num = len(self.data)
        if num > 0:
            dataset = list(self._generate_datalist())
            mean = self.pre_processing(dataset)
            if(mean is None):
                res_sum = sum(dataset)
                mean = res_sum / num
                std = sqrt(reduce(lambda summa, x: summa + (x - mean) ** 2, dataset, 0) / num)
                for i in dataset:
                    if mean - std > i or i > mean + std:
                        res_sum -= i
                        num -= 1
                if num > 0:
                    mean = res_sum / num
                else:
                    mean = np.nan
        else:
            mean = np.nan

        return mean

