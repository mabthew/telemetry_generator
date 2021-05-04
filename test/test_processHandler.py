import unittest
import datetime
import pwd
import os
from handlers import processHandler
from handlers import logWriter


class TestFileHandler(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        logWriter.LogWriter.getInstance()

    def setUp(self):
        self.cleanUp()

        timestamp = datetime.datetime.now()
        username = pwd.getpwuid(os.getuid())[0]
        
        self.p = processHandler.ProcessHandler(timestamp, username)

    def tearDown(self):
        self.cleanUp()

    def cleanUp(self):
        pass

    def test_run_valid_command(self):
        result = self.p.run("ls")
        self.assertTrue( result, "call did not execute")

    def test_run_invalid_command(self):
        result = self.p.run("abc123")   # assuming there is no file named abc123 in the directory tests are run from
        self.assertFalse( result, "call executed when it shouldn't have")

    def test_run_empty_command(self):
        result = self.p.run("")
        self.assertFalse( result, "call executed when it shouldn't have")
    
    def test_run_sets_process_info(self):
        result = self.p.run("ls")
        
        self.assertIsNotNone(self.p.process_id)
        self.assertIsNotNone(self.p.process_name)
        self.assertIsNotNone(self.p.command_line)
    
    

if __name__ == '__main__':
    unittest.main()
