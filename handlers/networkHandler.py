import subprocess
import sys
import os
import json
import psutil
import socket
import requests
import validators
import ctypes
from multiprocessing import Process, Value
from .abstractHandler import AbstractHandler


class NetworkHandler(AbstractHandler):
    def __init__(self, timestamp, username):
        super().__init__(timestamp, username)
        self.protocol = "TCP"

    def validateArgs(self, args):
        argList = args.lstrip().rstrip().split(" ")

        if len(argList) == 2:
            return True, argList[0], argList[1], ""
        elif len(argList) == 3:
            content = " ".join(argList[2:]).rstrip()
            if (content[0] == "\"" and content[-1] == "\""):
                return True, argList[0], argList[1], content[1:-1]
            return False, "", "", ""
        else:
            return False, argList[0], "", ""

    # create process
    def send(self, args):
        
        valid, address, port, data = self.validateArgs(args)

        self.destination_address = address
        self.size = len(data.encode('utf-8'))   # size of data in bytes

        if not port.isnumeric():
            print("\n Invalid port.\n")
            return False
        else:
            self.destination_port = int(port)

        if valid:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((address, int(port)))
               
            except:
                print("Socket failed to connect. Check that address and port are correct.") # TODO: better error handling
                return False

            socketInfo = s.getsockname()

            self.source_address = socketInfo[0]
            self.source_port = socketInfo[1]
            p = Process(target=self.sendData, args=[s, address, data])
            
        else:
            print("\n Invalid input. See 'help'.\n")
            return False
        
        p.start()

        # extract process info
        self.getProcessInfo(p.pid)        

        p.join()  # this blocks until the process terminates
    
        return True

    def sendData(self, s, address, data):
        s.send(b'hello')
        s.close()

    def log(self):
        res = json.dumps({
            "timestamp": str(self.timestamp),
            "username": self.username,
            "destination_address": self.destination_address,
            "destination_port": self.destination_port,
            "source_address": self.source_address,
            "source_port": self.source_port,
            "protocol": self.protocol,
            "size": self.size,
            "process_name": self.process_name,
            "command_line": self.command_line,
            "process_id": self.process_id
        })
        
        self.writer.logMetric(res)
