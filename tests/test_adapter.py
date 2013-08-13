import unittest

from betamax.adapter import VCRAdapter
from requests.adapters import HTTPAdapter


class TestVCRAdapter(unittest.TestCase):
    def setUp(self):
        self.adapter = VCRAdapter()

    def tearDown(self):
        self.adapter.eject_cassette()

    def test_has_http_adatper(self):
        assert self.adapter.http_adapter is not None
        assert isinstance(self.adapter.http_adapter, HTTPAdapter)

    def test_empty_initial_state(self):
        assert self.adapter.cassette is None
        assert self.adapter.cassette_name is None
        assert self.adapter.serialize is None

    def test_load_cassette(self):
        filename = 'vcr/cassettes/test.json'
        self.adapter.load_cassette(filename, 'json', {})
        assert self.adapter.cassette is not None
        assert self.adapter.cassette_name == filename
