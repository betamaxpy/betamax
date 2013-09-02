import os
import unittest

from requests import Session


class IntegrationHelper(unittest.TestCase):
    def setUp(self):
        self.cassette_path = None
        self.session = Session()

    def tearDown(self):
        assert self.cassette_path is not None
        os.unlink(self.cassette_path)
