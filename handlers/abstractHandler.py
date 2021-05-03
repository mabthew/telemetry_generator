from abc import ABC, abstractmethod


class AbstractHandler(ABC):
    def __init__(self, timestamp, username):
        self.timestamp = timestamp
        self.username = username

    @abstractmethod
    def log(self):
        pass
