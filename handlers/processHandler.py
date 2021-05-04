import subprocess
import sys
import os
import json
import psutil
from .abstractHandler import AbstractHandler

class ProcessHandler(AbstractHandler):
    def __init__(self, timestamp, username):
        super().__init__(timestamp, username)

    # create process
    def run(self, command):
        try:
            parsedCommand = command.split(' ')
            # create subprocess to execute command
            p = subprocess.Popen(parsedCommand)

            # extract process info
            self.process_id = p.pid
            ps = psutil.Process(p.pid)
            self.process_name = ps.name()
            self.command_line = ps.exe()

            p.wait()
            return True

        except FileNotFoundError:
            print('\nInvalid command: file not found error.\n')
            return False
        except PermissionError:
            print('\nInvalid command: permission denied error.\n')
            return False
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

    def log(self):
        res = json.dumps({
            "timestamp": str(self.timestamp),
            "username": self.username,
            "process_name": self.process_name,
            "command_line": self.command_line,
            "process_id": self.process_id
        })
        
        self.writer.logMetric(res)
