import os
import sys
import unittest

# sys.path.insert(0, os.path.abspath('.'))
# sys.stderr.write('%s' % str(sys.path))

from betamax.adapter import BetamaxAdapter
from requests.adapters import HTTPAdapter


class TestBetamaxAdapter(unittest.TestCase):
    def setUp(self):
        self.adapter = BetamaxAdapter()

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
        filename = 'tests/cassettes/test.json'
        self.adapter.load_cassette(filename, 'json', {
            'record': 'none'
        })
        assert self.adapter.cassette is not None
        assert self.adapter.cassette_name == filename


if __name__ == '__main__':
    sys.path.insert(0, os.path.abspath('../..'))
    unittest.main()
