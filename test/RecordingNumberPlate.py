class RecordingNumberPlate:
    def __init__(self, numberplate, time, date):
        self.numberplate = numberplate
        self.time = time
        self.date = date

    def __str__(self):
        return f"{self.numberplate}\t{self.time}\t{self.date}"
