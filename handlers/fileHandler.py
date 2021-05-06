import os
import json
import time
import psutil
from multiprocessing import Process, Value

from .abstractHandler import AbstractHandler


class FileHandler(AbstractHandler):
    def __init__(self, timestamp, username):
        super().__init__(timestamp, username)
        self.path = ''
        self.activity_descriptor = ''
        self.process_name = ''
        self.command_line = ''
        self.process_id = -1

    def validateArgs(self, args):
        argList = args.lstrip().rstrip().split(" ")
        if len(argList) == 1:
            return True, argList[0], ""
        else:
            content = " ".join(argList[1:]).rstrip()
            if (content[0] == "\"" and content[-1] == "\""):
                return True, argList[0], content[1:-1]
            return False, "", ""

    def call(self, method, args):
        valid, path, content = self.validateArgs(args)
        self.path = path

        # stores whether or not the requested function actually executes (since a new thread is being spawned it can't be treated as a basic variable)
        executed = Value('i', False)

        if valid:
            if method == "create":
                p = Process(target=self.create, args=[path, content, executed])
                self.activity_descriptor = "created"
            elif method == "modify":
                p = Process(target=self.modify, args=[path, content, executed])
                self.activity_descriptor = "modified"
            elif method == "delete":
                p = Process(target=self.delete, args=[args, executed])
                self.activity_descriptor = "deleted"
            else:
                raise Exception("Unimplemented file handling function.")
        else:
            print("\n Invalid input. See 'help'.\n")
            return False

        p.start()

        # extract process info
        self.getProcessInfo(p.pid)

        p.join()  # this blocks until the process terminates

        # return whether or not executed for logging purposes
        return bool(executed.value)

    # create file
    def create(self, path, content, executed):
        if os.path.exists(path):
            print("File already exists")
        else:
            f = open(path, "w+")
            f.write(content)
            f.close()
            print("File created")
            executed.value = True

    # append to file, create if not exist
    def modify(self, path, content, executed):
        if os.path.exists(path):
            f = open(path, "a")
            f.write(content)
            print("Appended to file")
        else:
            f = open(path, "w+")
            f.write(content)
            f.close()
            print("File created")
        executed.value = True
        f.close()

    # delete file
    def delete(self, path, executed):
        self.path = path

        if os.path.exists(path):
            os.remove(path)
            print("File Deleted")
            executed.value = True
        else:
            print("path: \'" + path + "\': does not exist")

    def getFullPath(self):
        pass

    def log(self):
        res = json.dumps({
            "timestamp": str(self.timestamp),
            "path": self.path,
            "activity_descriptor": self.activity_descriptor,
            "username": self.username,
            "process_name": self.process_name,
            "command_line": self.command_line,
            "process_id": self.process_id
        })

        self.writer.logMetric(res)
