import unittest
import datetime
import pwd
import os
from handlers import processHandler
from handlers import logger


class TestProcessHandler(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        writer = logger.Logger.getInstance()

    def setUp(self):
        self.cleanUp()

        timestamp = datetime.datetime.now()
        username = pwd.getpwuid(os.getuid())[0]
        
        self.handler = processHandler.ProcessHandler(timestamp, username)

    def tearDown(self):
        self.cleanUp()

    def cleanUp(self):
        pass

    def test_run_valid_command(self):
        result = self.handler.run("ls")
        self.assertTrue( result, "call did not execute")

    def test_run_invalid_command(self):
        result = self.handler.run("abc123")   # assuming there is no file named abc123 in the directory tests are run from
        self.assertFalse( result, "call executed when it shouldn't have")

    def test_run_empty_command(self):
        result = self.handler.run("")
        self.assertFalse( result, "call executed when it shouldn't have")
    
    def test_run_sets_process_log_info(self):
        result = self.handler.run("ls")

        self.assertIsNotNone(self.handler.timestamp)
        self.assertIsNotNone(self.handler.username)
        self.assertIsNotNone(self.handler.process_name)
        self.assertIsNotNone(self.handler.command_line)
        self.assertIsNotNone(self.handler.process_id)
  
if __name__ == '__main__':
    unittest.main()
