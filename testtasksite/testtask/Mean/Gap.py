from datetime import datetime


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