from abc import ABC, abstractmethod
from .logWriter import LogWriter

class AbstractHandler(ABC):
    def __init__(self, timestamp, username):
        self.timestamp = timestamp
        self.username = username
        self.writer = LogWriter.getInstance()

    @abstractmethod
    def log(self):
        pass
