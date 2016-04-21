import unittest

try:
    from unittest import mock
except ImportError:
    import mock

from betamax.adapter import BetamaxAdapter
from requests.adapters import HTTPAdapter
from requests.models import PreparedRequest


class TestBetamaxAdapter(unittest.TestCase):
    def setUp(self):
        http_adapter = mock.Mock()
        self.adapters_dict = {'http://': http_adapter}
        self.adapter = BetamaxAdapter(old_adapters=self.adapters_dict)

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
        filename = 'test'
        self.adapter.load_cassette(filename, 'json', {
            'record': 'none',
            'cassette_library_dir': 'tests/cassettes/'
        })
        assert self.adapter.cassette is not None
        assert self.adapter.cassette_name == filename

    def test_prerecord_hook(self):
        cassette = mock.Mock()
        cassette.interactions = ['fake']
        self.adapter.cassette = cassette
        request = PreparedRequest()
        request.url = 'http://example.com'
        response = object()
        adapter = self.adapters_dict['http://']
        adapter.send.return_value = response

        with mock.patch('betamax.cassette.dispatch_hooks') as dispatch_hooks:
            self.adapter.send_and_record(request)

        adapter.send.assert_called_once_with(
            request, stream=True, timeout=None, verify=True, cert=None,
            proxies=None,
        )

        dispatch_hooks.assert_called_once_with(
            'before_record', response, cassette,
        )

    def test_preplayback_hook(self):
        interaction = mock.Mock()
        cassette = mock.Mock()
        cassette.find_match.return_value = interaction
        self.adapter.cassette = cassette
        request = PreparedRequest()
        request.url = 'http://example.com'

        with mock.patch('betamax.cassette.dispatch_hooks') as dispatch_hooks:
            self.adapter.send(request)

        dispatch_hooks.assert_called_once_with(
            'before_playback', interaction, cassette
        )
