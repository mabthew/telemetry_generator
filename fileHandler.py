import os


class FileHandler:
    def __init__(self):
        self.data = []

    # create file
    def create(self, path):
        f = open(path, "w+")
        f.close()
        print("File created")

    # modify file, create if not exist
    # TODO: implement modify
    def modify(self, path):
        f = open(path, "w+")
        f.close()
        print("File created")

    # delete file
    def delete(self, path):
        if os.path.exists(path):
            os.remove(path)
            print("File Deleted")
        else:
            print("path: \'" + path + "\': does not exist")
