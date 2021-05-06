import unittest
import datetime
import pwd
import os
from handlers import networkHandler
from handlers import logWriter


class TestNetworkHandler(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        logWriter.LogWriter.getInstance()

    def setUp(self):
        self.cleanUp()

        timestamp = datetime.datetime.now()
        username = pwd.getpwuid(os.getuid())[0]
        
        self.handler = networkHandler.NetworkHandler(timestamp, username)

    def tearDown(self):
        self.cleanUp()

    def cleanUp(self):
        pass

    def test_send_valid_request_no_text(self):
        result = self.handler.send("google.com 80")
        self.assertTrue( result, "call did not execute")

    def test_send_valid_request_with_text(self):
        result = self.handler.send("google.com 80 \"text\"")
        self.assertTrue( result, "call did not execute")

    def test_run_invalid_command(self):
        result = self.handler.send("invalid_command")
        self.assertFalse( result, "call executed when it shouldn't have")

    def test_run_empty_command(self):
        result = self.handler.send("")
        self.assertFalse( result, "call executed when it shouldn't have")
    
    def test_run_sets_process_info(self):
        result = self.handler.send("google.com 80")
          
        self.assertIsNotNone(self.handler.timestamp)
        self.assertIsNotNone(self.handler.username)
        self.assertIsNotNone(self.handler.destination_address)
        self.assertIsNotNone(self.handler.destination_port)
        self.assertIsNotNone(self.handler.source_address)
        self.assertIsNotNone(self.handler.source_port)
        self.assertIsNotNone(self.handler.size)
        self.assertIsNotNone(self.handler.protocol)
        self.assertIsNotNone(self.handler.process_name)
        self.assertIsNotNone(self.handler.command_line)
        self.assertIsNotNone(self.handler.process_id)
    
    

if __name__ == '__main__':
    unittest.main()
