import unittest

from betamax import VCR, matchers
from betamax.adapter import VCRAdapter
from betamax.cassette import Cassette
from requests import Session
from requests.adapters import HTTPAdapter


class TestVCR(unittest.TestCase):
    def setUp(self):
        self.session = Session()
        self.vcr = VCR(self.session)

    def test_initialization_does_alter_the_session(self):
        assert not isinstance(self.session.adapters['http://'], VCRAdapter)
        assert isinstance(self.session.adapters['http://'], HTTPAdapter)
        assert not isinstance(self.session.adapters['https://'], VCRAdapter)
        assert isinstance(self.session.adapters['https://'], HTTPAdapter)

    def test_entering_context_alters_adapters(self):
        with self.vcr:
            assert isinstance(self.session.adapters['http://'], VCRAdapter)
            assert isinstance(self.session.adapters['https://'], VCRAdapter)

    def test_exiting_resets_the_adapters(self):
        with self.vcr:
            assert isinstance(self.session.adapters['http://'], VCRAdapter)
            assert isinstance(self.session.adapters['https://'], VCRAdapter)
        assert not isinstance(self.session.adapters['http://'], VCRAdapter)
        assert not isinstance(self.session.adapters['https://'], VCRAdapter)

    def test_current_cassette(self):
        assert self.vcr.current_cassette is None
        self.vcr.use_cassette('test')
        assert isinstance(self.vcr.current_cassette, Cassette)

    def test_use_cassette_returns_cassette_object(self):
        assert self.vcr.use_cassette('test') is self.vcr

    def test_register_request_matcher(self):
        class FakeMatcher(object):
            name = 'fake'

        VCR.register_request_matcher(FakeMatcher)
        assert 'fake' in matchers.matcher_registry
        assert isinstance(matchers.matcher_registry['fake'], FakeMatcher)

    def test_stores_the_session_instance(self):
        assert self.session is self.vcr.session
