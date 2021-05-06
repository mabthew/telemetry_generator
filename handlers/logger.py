import os
from pathlib import Path

class Logger:
    __instance = None

    @staticmethod 
    def getInstance():
        # static access method
        if Logger.__instance == None:
            Logger()
        return Logger.__instance

    def __init__(self, path):
        self.path = path
        if Logger.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            Logger.__instance = self


    # add item to json list   
    def logMetric(self, metric):
        with open(self.path, 'a') as f:
            f.write("\n\t" + metric + ",")   

    # open json list
    def openLog(self):
        Path("./logs").mkdir(parents=True, exist_ok=True)   # create logs directory if not
        with open(self.path, 'a') as f:
             f.write("[ ")


    # close json list
    def closeLog(self):
        with open(self.path, 'rb+') as f:
            f.seek(-1, os.SEEK_END)
            f.truncate()    # remove trailing comma at end of program execution
            f.write(b"\n]")
