import unittest

from requests import PreparedRequest
from betamax import matchers


class TestMatchers(unittest.TestCase):
    def setUp(self):
        self.alt_url = ('http://example.com/path/to/end/point?query=string'
                        '&foo=bar')
        self.p = PreparedRequest()
        self.p.body = 'Foo bar'
        self.p.headers = {'User-Agent': 'betamax/test'}
        self.p.url = 'http://example.com/path/to/end/point?query=string'
        self.p.method = 'GET'

    def test_matcher_registry_has_body_matcher(self):
        assert 'body' in matchers.matcher_registry

    def test_matcher_registry_has_headers_matcher(self):
        assert 'headers' in matchers.matcher_registry

    def test_matcher_registry_has_host_matcher(self):
        assert 'host' in matchers.matcher_registry

    def test_matcher_registry_has_method_matcher(self):
        assert 'method' in matchers.matcher_registry

    def test_matcher_registry_has_path_matcher(self):
        assert 'path' in matchers.matcher_registry

    def test_matcher_registry_has_query_matcher(self):
        assert 'query' in matchers.matcher_registry

    def test_matcher_registry_has_uri_matcher(self):
        assert 'uri' in matchers.matcher_registry

    def test_body_matcher(self):
        match = matchers.matcher_registry['body'].match
        assert match(self.p, {'body': 'Foo bar'})
        assert match(self.p, {'body': ''}) is False

    def test_headers_matcher(self):
        match = matchers.matcher_registry['headers'].match
        assert match(self.p, {'headers': {'User-Agent': 'betamax/test'}})
        assert match(self.p, {'headers': {'X-Sha': '6bbde0af'}}) is False

    def test_host_matcher(self):
        match = matchers.matcher_registry['host'].match
        assert match(self.p, {'uri': 'http://example.com'})
        assert match(self.p, {'uri': 'https://example.com'})
        assert match(self.p, {'uri': 'https://example.com/path'})
        assert match(self.p, {'uri': 'https://example2.com'}) is False

    def test_method_matcher(self):
        match = matchers.matcher_registry['method'].match
        assert match(self.p, {'method': 'GET'})
        assert match(self.p, {'method': 'POST'}) is False

    def test_path_matcher(self):
        match = matchers.matcher_registry['path'].match
        assert match(self.p, {'uri': 'http://example.com/path/to/end/point'})
        assert match(self.p,
                     {'uri': 'http://example.com:8000/path/to/end/point'})
        assert match(self.p,
                     {'uri': 'http://example.com:8000/path/to/end/'}) is False

    def test_query_matcher(self):
        match = matchers.matcher_registry['query'].match
        assert match(
            self.p,
            {'uri': 'http://example.com/path/to/end/point?query=string'}
        )
        assert match(
            self.p,
            {'uri': 'http://example.com/?query=string'}
        )
        self.p.url = self.alt_url
        assert match(
            self.p,
            {'uri': self.alt_url}
        )
        # Regression test (order independence)
        assert match(
            self.p,
            {'uri': 'http://example.com/?foo=bar&query=string'}
        )
        # Regression test (no query issue)
        assert match(self.p, {'uri': 'http://example.com'}) is False

    def test_uri_matcher(self):
        match = matchers.matcher_registry['uri'].match
        assert match(
            self.p,
            {'uri': 'http://example.com/path/to/end/point?query=string'}
        )
        assert match(self.p, {'uri': 'http://example.com'}) is False

    def test_uri_matcher_handles_query_strings(self):
        match = matchers.matcher_registry['uri'].match
        self.p.url = 'http://example.com/path/to?query=string&form=value'
        other_uri = 'http://example.com/path/to?form=value&query=string'
        assert match(self.p, {'uri': other_uri}) is True


class TestBaseMatcher(unittest.TestCase):
    def setUp(self):
        class Matcher(matchers.BaseMatcher):
            pass
        self.Matcher = Matcher

    def test_requires_name(self):
        self.assertRaises(ValueError, self.Matcher)

    def test_requires_you_overload_match(self):
        self.Matcher.name = 'test'
        m = self.Matcher()
        self.assertRaises(NotImplementedError, m.match, None, None)
