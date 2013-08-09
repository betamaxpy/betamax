import unittest

from requests import PreparedRequest
from requests_vcr.matchers import matcher_registry


class TestMatchers(unittest.TestCase):
    def setUp(self):
        self.alt_url = ('http://example.com/path/to/end/point?query=string'
                        '&foo=bar')
        self.p = PreparedRequest()
        self.p.body = 'Foo bar'
        self.p.headers = {'User-Agent': 'requests-vcr/test'}
        self.p.url = 'http://example.com/path/to/end/point?query=string'
        self.p.method = 'GET'

    def test_matcher_registry_has_body_matcher(self):
        assert 'body' in matcher_registry

    def test_matcher_registry_has_headers_matcher(self):
        assert 'headers' in matcher_registry

    def test_matcher_registry_has_host_matcher(self):
        assert 'host' in matcher_registry

    def test_matcher_registry_has_method_matcher(self):
        assert 'method' in matcher_registry

    def test_matcher_registry_has_path_matcher(self):
        assert 'path' in matcher_registry

    def test_matcher_registry_has_query_matcher(self):
        assert 'query' in matcher_registry

    def test_matcher_registry_has_uri_matcher(self):
        assert 'uri' in matcher_registry

    def test_body_matcher(self):
        match = matcher_registry['body'].match
        assert match(self.p, {'body': 'Foo bar'})
        assert match(self.p, {'body': ''}) is False

    def test_headers_matcher(self):
        match = matcher_registry['headers'].match
        assert match(self.p, {'headers': {'User-Agent': 'requests-vcr/test'}})
        assert match(self.p, {'headers': {'X-Sha': '6bbde0af'}}) is False

    def test_host_matcher(self):
        match = matcher_registry['host'].match
        assert match(self.p, {'url': 'http://example.com'})
        assert match(self.p, {'url': 'https://example.com'})
        assert match(self.p, {'url': 'https://example.com/path'})
        assert match(self.p, {'url': 'https://example2.com'}) is False

    def test_method_matcher(self):
        match = matcher_registry['method'].match
        assert match(self.p, {'method': 'GET'})
        assert match(self.p, {'method': 'POST'}) is False

    def test_path_matcher(self):
        match = matcher_registry['path'].match
        assert match(self.p, {'url': 'http://example.com/path/to/end/point'})
        assert match(self.p,
                     {'url': 'http://example.com:8000/path/to/end/point'})
        assert match(self.p,
                     {'url': 'http://example.com:8000/path/to/end/'}) is False

    def test_query_matcher(self):
        match = matcher_registry['query'].match
        assert match(
            self.p,
            {'url': 'http://example.com/path/to/end/point?query=string'}
        )
        assert match(
            self.p,
            {'url': 'http://example.com/?query=string'}
        )
        self.p.url = self.alt_url
        assert match(
            self.p,
            {'url': self.alt_url}
        )
        assert match(
            self.p,
            {'url': 'http://example.com/?foo=bar&query=string'}
        )
