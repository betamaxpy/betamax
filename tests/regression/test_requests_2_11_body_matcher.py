import os
import unittest

from betamax import Betamax
from requests import Session


class TestRequests211BodyMatcher(unittest.TestCase):
    def tearDown(self):
        os.unlink('tests/cassettes/requests_2_11_body_matcher.json')

    def test_requests_with_json_body(self):
        s = Session()
        with Betamax(s).use_cassette('requests_2_11_body_matcher',
                                     match_requests_on=['body']):
            r = s.post('https://httpbin.org/post', json={'a': 2})
            assert r.json() is not None

        s = Session()
        with Betamax(s).use_cassette('requests_2_11_body_matcher',
                                     match_requests_on=['body']):
            r = s.post('https://httpbin.org/post', json={'a': 2})
            assert r.json() is not None
