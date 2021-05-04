import unittest
import datetime
import pwd
import os
from handlers import fileHandler


class TestFileHandler(unittest.TestCase):
    def setUp(self):
        self.cleanUp()
        timestamp = datetime.datetime.now()
        username = pwd.getpwuid(os.getuid())[0]
        self.f = fileHandler.FileHandler(timestamp, username)

    def tearDown(self):
        self.cleanUp()

    def cleanUp(self):
        self.path = "test.txt"
        if os.path.exists(self.path):
            os.remove(self.path)

    def test_file_create(self):
        self.f.create(self.path, "")


if __name__ == '__main__':
    unittest.main()
