import os
import sys
import json
import psutil
import subprocess

from .abstractHandler import AbstractHandler

class ProcessHandler(AbstractHandler):
    def __init__(self, timestamp, username):
        super().__init__(timestamp, username)
        self.process_name = ''
        self.command_line = ''
        self.process_id = -1

    # create process
    def run(self, command):
        try:
            parsedCommand = command.split(" ")
            # create subprocess to execute command
            p = subprocess.Popen(parsedCommand)

            # extract process info
            self.getProcessInfo(p.pid)

            p.wait()
            return True

        except FileNotFoundError:
            print('\nInvalid command: file not found error.\n')
            return False
        except PermissionError:
            print('\nInvalid command: permission denied error.\n')
            return False
        except:
            print("\nUnexpected error:", sys.exc_info()[0])
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
