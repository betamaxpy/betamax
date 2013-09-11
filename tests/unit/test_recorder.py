import unittest

from betamax import matchers
from betamax.adapter import BetamaxAdapter
from betamax.cassette import Cassette
from betamax.recorder import Betamax, Options
from requests import Session
from requests.adapters import HTTPAdapter


class TestBetamax(unittest.TestCase):
    def setUp(self):
        self.session = Session()
        self.vcr = Betamax(self.session)

    def test_initialization_does_not_alter_the_session(self):
        for v in self.session.adapters.values():
            assert not isinstance(v, BetamaxAdapter)
            assert isinstance(v, HTTPAdapter)

    def test_entering_context_alters_adapters(self):
        with self.vcr:
            for v in self.session.adapters.values():
                assert isinstance(v, BetamaxAdapter)

    def test_exiting_resets_the_adapters(self):
        with self.vcr:
            pass
        for v in self.session.adapters.values():
            assert not isinstance(v, BetamaxAdapter)

    def test_current_cassette(self):
        assert self.vcr.current_cassette is None
        self.vcr.use_cassette('test')
        assert isinstance(self.vcr.current_cassette, Cassette)

    def test_use_cassette_returns_cassette_object(self):
        assert self.vcr.use_cassette('test') is self.vcr

    def test_register_request_matcher(self):
        class FakeMatcher(object):
            name = 'fake'

        Betamax.register_request_matcher(FakeMatcher)
        assert 'fake' in matchers.matcher_registry
        assert isinstance(matchers.matcher_registry['fake'], FakeMatcher)

    def test_stores_the_session_instance(self):
        assert self.session is self.vcr.session


class TestOptions(unittest.TestCase):
    def setUp(self):
        self.data = {
            're_record_interval': 10000,
            'match_requets_on': ['match'],
            'serialize': 'json'
        }
        self.options = Options(self.data)

    def test_data_is_valid(self):
        for key in self.data:
            assert key in self.options

    def test_invalid_data_is_removed(self):
        data = self.data.copy()
        data['fake'] = 'value'
        options = Options(data)

        for key in self.data:
            assert key in options

        assert 'fake' not in options
