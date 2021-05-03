import subprocess
import sys


class ProcessHandler:
    def __init__(self):
        self.data = []

    # create process
    def run(self, command):
        try:
            parsedCommand = command.split(' ')
            subprocess.call(parsedCommand)
        except FileNotFoundError:
            print('\nInvalid command: file not found error.\n')
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise
