import subprocess
import sys
import os
import psutil
import json
import abstractHandler


class ProcessHandler(abstractHandler.AbstractHandler):
    def __init__(self, timestamp, username):
        super().__init__(timestamp, username)

    # create process
    def run(self, command):
        try:
            parsedCommand = command.split(' ')
            p = subprocess.Popen(parsedCommand)

            ps = psutil.Process(p.pid)
            self.process_id = p.pid
            self.process_name = ps.name()
            self.command_line = ps.exe()

            p.wait()
        except FileNotFoundError:
            print('\nInvalid command: file not found error.\n')
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
