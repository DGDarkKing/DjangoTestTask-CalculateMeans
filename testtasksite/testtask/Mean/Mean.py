from abc import ABC, abstractmethod

import numpy as np


class Mean(ABC):

    @abstractmethod
    def __init__(self, target, data):
        self.target = target
        self.data = data

    @abstractmethod
    def compute(self):
        pass

    def _generate_datalist(self):
        if self.target is None:
            return self.data
        elif self.data is None or (self.data) == 0:
            return self.data

        return (el[self.target] for el in self.data)

    def get_sample(self):
        if self.data is None or (self.data) == 0:
            return None
        elif self.target is None:
            return self.data[0]

        return self.data[self.target]

    @staticmethod
    def pre_processing(data):
        n = len(data)
        if n == 0:
            return np.nan
        elif n == 1:
            return data[0]
        elif n == 2:
            return (data[0]+data[1]) / 2
        else:
            return None
