import unittest
import datetime
import pwd
import os
from handlers import fileHandler
from handlers import logWriter


class TestFileHandler(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        logWriter.LogWriter("output.json")

    def setUp(self):
        self.cleanUp()

        timestamp = datetime.datetime.now()
        username = pwd.getpwuid(os.getuid())[0]
        
        self.f = fileHandler.FileHandler(timestamp, username)

    def tearDown(self):
        self.cleanUp()

    def cleanUp(self):
        self.relative_path = "test.txt"
        self.absolute_path = os.getcwd() + "/test.txt"

        if os.path.exists(self.relative_path):
            os.remove(self.relative_path)

    # create file functionality
    def test_call_create_relative_path(self):
        result = self.f.call("create", self.relative_path)
        self.assertTrue( result, "call did not execute")
    
    def test_call_create_absolute_path(self):
        result = self.f.call("create", self.absolute_path)
        self.assertTrue( result, "call did not execute")

    def test_call_create_relative_path(self):
        result = self.f.call("create", self.relative_path)
        self.assertTrue( result, "call did not execute")
    
    def test_call_create_invalid_path(self):
        result = self.f.call("create", "~/invalid_path")
        self.assertFalse( result, "call executed when it shouldn't have")
    
    def test_call_create_sets_process_info(self):
        result = self.f.call("create", self.relative_path)
        
        self.assertIsNotNone(self.f.process_id)
        self.assertIsNotNone(self.f.process_name)
        self.assertIsNotNone(self.f.command_line)

    # modify file functionality
    def test_call_modify_on_existing_relative_path(self):
        f = open(self.relative_path, "w+")
        f.close()
        result = self.f.call("modify", self.relative_path)
        self.assertTrue( result, "call did not execute")

    def test_call_modify_on_existing_absolute_path(self):
        f = open(self.absolute_path, "w+")
        f.close()
        result = self.f.call("modify", self.absolute_path)
        self.assertTrue( result, "call did not execute")
    
    def test_call_modify_on_nonexistant_file(self):
        result = self.f.call("modify", self.relative_path)
        self.assertTrue( result, "call did not execute")

    def test_call_modify_invalid_path(self):
        result = self.f.call("modify", "~/invalid_path")
        self.assertFalse( result, "call executed when it shouldn't have")

    def test_call_modify_sets_process_info(self):
        result = self.f.call("modify", self.relative_path)
        
        self.assertIsNotNone(self.f.process_id)
        self.assertIsNotNone(self.f.process_name)
        self.assertIsNotNone(self.f.command_line)

    # delete file functionality
    def test_call_delete_on_existing_relative_path(self):
        f = open(self.relative_path, "w+")
        f.close()
        result = self.f.call("delete", self.relative_path)
        self.assertTrue( result, "call did not execute")

    def test_call_delete_on_existing_absolute_path(self):
        f = open(self.absolute_path, "w+")
        f.close()
        result = self.f.call("delete", self.absolute_path)
        self.assertTrue( result, "call did not execute")
    
    def test_call_delete_on_nonexistant_file(self):
        result = self.f.call("delete", self.relative_path)
        self.assertFalse( result, "call executed when it shouldn't have")

    def test_call_delete_invalid_path(self):
        result = self.f.call("delete", "~/invalid_path")
        self.assertFalse( result, "call executed when it shouldn't have")
    
    def test_call_delete_sets_process_info(self):
        f = open(self.relative_path, "w+")
        f.close()
        result = self.f.call("delete", self.relative_path)
        
        self.assertIsNotNone(self.f.process_id)
        self.assertIsNotNone(self.f.process_name)
        self.assertIsNotNone(self.f.command_line)

    # call method functionality
    def test_call_invalid_method(self):
        with self.assertRaises(Exception):
            self.f.call("invalid_method", self.relative_path)
    
    def test_call_no_method(self):
        with self.assertRaises(Exception):
            self.f.call(None, self.relative_path)
    

if __name__ == '__main__':
    unittest.main()
