import os
import pwd
import json
import unittest
import datetime
from handlers import logger
from handlers import fileHandler
from handlers import processHandler
from handlers import networkHandler

class TestLogWriter(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        logger.Logger.getInstance()

    def setUp(self):
        self.cleanUp()
        self.writer = logger.Logger.getInstance()

        timestamp = datetime.datetime.now()
        username = pwd.getpwuid(os.getuid())[0]
        
        self.fileHandler = fileHandler.FileHandler(timestamp, username)
        self.processHandler = processHandler.ProcessHandler(timestamp, username)
        self.networkHandler = networkHandler.NetworkHandler(timestamp, username)

    def tearDown(self):
        self.cleanUp()

    def cleanUp(self):
        self.log_file = "logs.json"
        self.relative_path_file = "test.txt"

        if os.path.exists(self.log_file):
            os.remove(self.log_file)

        if os.path.exists(self.relative_path_file):
            os.remove(self.relative_path_file)


    # process log tests
    def test_run_process_generates_logs(self):
        timestamp = datetime.datetime.now()
        username = pwd.getpwuid(os.getuid())[0]
        
        success = self.processHandler.run("ls")

        if success:
            self.writer.openLog()
            self.processHandler.log()
            self.writer.closeLog()
        else:
            self.fail("un process did not execute")

        with open(self.log_file) as f:
            data = json.load(f)[0]

        self.assertIn("timestamp", data)
        self.assertIn("username", data)
        self.assertIn("process_name", data)
        self.assertIn("command_line", data)
        self.assertIn("process_id", data)

    # file log tests
    def test_create_file_generates_logs(self):
        timestamp = datetime.datetime.now()
        username = pwd.getpwuid(os.getuid())[0]
        
        success = self.fileHandler.call("create", self.relative_path_file)

        if success:
            self.writer.openLog()
            self.fileHandler.log()
            self.writer.closeLog()
        else:
            pass

        with open(self.log_file) as f:
            data = json.load(f)[0]

        self.assertIn("timestamp", data)
        self.assertIn("username", data)
        self.assertIn("path", data)
        self.assertIn("activity_descriptor", data)
        self.assertEqual(data["activity_descriptor"], "created")
        self.assertIn("process_name", data)
        self.assertIn("command_line", data)
        self.assertIn("process_id", data)

    def test_modify_file_generates_logs(self):
        timestamp = datetime.datetime.now()
        username = pwd.getpwuid(os.getuid())[0]
        
        success = self.fileHandler.call("modify", self.relative_path_file)

        if success:
            self.writer.openLog()
            self.fileHandler.log()
            self.writer.closeLog()
        else:
            self.fail("modify file did not execute")


        with open(self.log_file) as f:
            data = json.load(f)[0]

        self.assertIn("timestamp", data)
        self.assertIn("username", data)
        self.assertIn("process_name", data)
        self.assertIn("command_line", data)
        self.assertIn("process_id", data)


    def test_delete_file_generates_logs(self):
        timestamp = datetime.datetime.now()
        username = pwd.getpwuid(os.getuid())[0]

        f = open(self.relative_path_file, "w+")
        f.close()
        
        success = self.fileHandler.call("delete", self.relative_path_file)

        if success:
            self.writer.openLog()
            self.fileHandler.log()
            self.writer.closeLog()
        else:
            self.fail("delete file did not execute")

        with open(self.log_file) as f:
            data = json.load(f)[0]

        self.assertIn("timestamp", data)
        self.assertIn("username", data)
        self.assertIn("process_name", data)
        self.assertIn("command_line", data)
        self.assertIn("process_id", data)

    # network log tests
    def test_network_connect_generates_logs(self):
        timestamp = datetime.datetime.now()
        username = pwd.getpwuid(os.getuid())[0]

        f = open(self.relative_path_file, "w+")
        f.close()
        
        success = self.networkHandler.send("google.com 80 \"data\"")

        print('\n\n\n\n\n\nhello\n\n\n\n\n')
        print(success)
        if success:
            self.writer.openLog()
            self.networkHandler.log()
            self.writer.closeLog()
        else:
            self.fail("network connection did not execute")

        with open(self.log_file) as f:
            data = json.load(f)[0]

        self.assertIn("timestamp", data)
        self.assertIn("username", data)
        self.assertIn("process_name", data)
        self.assertIn("command_line", data)
        self.assertIn("process_id", data)
