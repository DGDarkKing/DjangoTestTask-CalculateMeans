import numpy as np

import testtask.BusnesLayer.Mean as Mean


class MyMean(Mean.Mean):

    def __init__(self, target=None, data=None):
        super(MyMean, self).__init__(target, data)

    def compute(self):
        num = len(self.data)
        if num > 0:
            dataset = list(self._generate_datalist())
            mean = self.pre_processing(dataset)
            if mean is None:
                mean = Mean.compute_mean_without_outliers(dataset)
        else:
            mean = np.nan
        return mean


