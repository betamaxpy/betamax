import os
import unittest

from betamax import Betamax
from requests import Session


class TestCassetteRecordMode(unittest.TestCase):
    def setUp(self):
        with Betamax.configure() as config:
            config.default_cassette_options['record_mode'] = 'never'

    def tearDown(self):
        os.unlink('tests/cassettes/regression_record_mode.json')

    def test_record_mode_is_never(self):
        s = Session()
        with Betamax(s).use_cassette('regression_record_mode') as recorder:
            assert recorder.current_cassette.record_mode == 'never'
