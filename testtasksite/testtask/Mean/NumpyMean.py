import numpy as np

from .Mean import Mean


class NumpyMean(Mean):

    def __init__(self, target=None, data=None):
        super(NumpyMean, self).__init__(target, data)

    def compute(self):
        # dataset = np.fromiter(self._generate_datalist(), dtype=int)
        dataset = list(self._generate_datalist())
        mean = self.pre_processing(dataset)

        if (mean is None):
            dataset = np.array(dataset)
            mean = np.mean(dataset)
            std = np.std(dataset)
            mean = np.mean(dataset, where=(mean - std <= dataset) & (dataset <= mean + std))

        return mean