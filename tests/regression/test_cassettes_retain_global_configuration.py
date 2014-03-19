import pytest
import unittest

from betamax import Betamax, new_cassette
from requests import Session


class TestCassetteRecordMode(unittest.TestCase):
    def setUp(self):
        with Betamax.configure() as config:
            config.default_cassette_options['record_mode'] = 'never'

    def tearDown(self):
        with Betamax.configure() as config:
            config.default_cassette_options['record_mode'] = 'once'

    def test_record_mode_is_never(self):
        s = Session()
        with pytest.raises(ValueError):
            with Betamax(s) as recorder:
                recorder.use_cassette('regression_record_mode')
                assert recorder.current_cassette is None

    def test_class_variables_retain_their_value(self):
        opts = new_cassette.NewCassette.default_cassette_options
        assert opts['record_mode'] == 'never'
