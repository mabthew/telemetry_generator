import os
import json
from .abstractHandler import AbstractHandler
from multiprocessing import Process
import psutil
import time


class FileHandler(AbstractHandler):
    def __init__(self, timestamp, username):
        super().__init__(timestamp, username)

    def validateArgs(self, args):
        argList = args.split(" ")
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
        if valid:
            if method == "create":
                p = Process(target=self.create, args=(path, content))
                self.activity_descriptor = "created"
            elif method == "modify":
                p = Process(target=self.modify, args=(path, content))
                self.activity_descriptor = "modified"
            elif method == "delete":
                p = Process(target=self.delete, args=(args,))
                self.activity_descriptor = "deleted"
            else:
                raise Exception("Unimplemented file handling function.")
        else:
            print("\n Invalid input. See 'help'.\n")
            return False

        p.start()

        # extract process info
        self.process_id = p.pid
        ps = psutil.Process(p.pid)
        self.process_name = ps.name()
        self.command_line = ps.exe()

        p.join()  # this blocks until the process terminates
        return True

    # create file
    def create(self, path, content):
        if os.path.exists(path):
            print("File already exists")
        else:
            f = open(path, "w+")
            f.write(content)
            f.close()
            print("File created")

    # append to file, create if not exist
    def modify(self, path, content):
        if os.path.exists(path):
            f = open(path, "a")
            f.write(content)
            print("Appended to file")
        else:
            f = open(path, "w+")
            f.write(content)
            f.close()
            print("File created")
        f.close()

    # delete file
    def delete(self, path):
        self.path = path

        if os.path.exists(path):
            os.remove(path)
            print("File Deleted")
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

        print(res)
