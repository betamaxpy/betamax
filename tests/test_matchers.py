import unittest

from requests_vcr.matchers import matcher_registry


class TestMatchers(unittest.TestCase):
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
