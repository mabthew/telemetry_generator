import os
from pathlib import Path

class LogWriter:
    __instance = None

    @staticmethod 
    def getInstance():
        """ Static access method. """
        if LogWriter.__instance == None:
            LogWriter()
        return LogWriter.__instance

    def __init__(self, path):
        self.path = path
        if LogWriter.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            LogWriter.__instance = self


    # add item to json list   
    def logMetric(self, metric):
        with open(self.path, 'a') as f:
            f.write("\n\t" + metric + ",")   

    # open json list
    def openLog(self):
        Path("./logs").mkdir(parents=True, exist_ok=True)   # create logs directory if not exist
        with open(self.path, 'a') as f:
             f.write("[ ")


    # close json list
    def closeLog(self):
        with open(self.path, 'rb+') as f:
            f.seek(-1, os.SEEK_END)
            f.truncate()    # remove trailing comma at end of program execution
            f.write(b"\n]")
