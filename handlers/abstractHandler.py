from abc import ABC, abstractmethod
import psutil
from .logWriter import LogWriter

class AbstractHandler(ABC):
    def __init__(self, timestamp, username):
        self.timestamp = timestamp
        self.username = username
        self.writer = LogWriter.getInstance()

    def getProcessInfo(self, pid):
        self.process_id = pid
        p = psutil.Process(pid)
        self.process_name = p.name()
        self.command_line = p.exe()

    @abstractmethod
    def log(self):
        pass
