import unittest

from betamax import Betamax
from betamax.matchers import HeadersMatcher
from requests import Session
from requests.auth import HTTPDigestAuth


class CustomHeadersMatcher(HeadersMatcher):
    name = 'custom-headers'

    def match(self, request, recorded_request):
        request_headers = dict(request.headers)
        recorded_headers = self.flatten_headers(recorded_request)
        self.remove_user_agent(request_headers)
        self.remove_user_agent(recorded_headers)
        return request_headers == recorded_headers

    def remove_user_agent(self, headers):
        try:
            del headers['User-Agent']
        except KeyError:
            del headers['user-agent']


Betamax.register_request_matcher(CustomHeadersMatcher)


class TestDigestAuth(unittest.TestCase):
    def test_saves_content_as_gzip(self):
        s = Session()
        cassette_name = 'handles_digest_auth'
        match = ['method', 'uri', 'custom-headers']
        with Betamax(s).use_cassette(cassette_name, match_requests_on=match):
            r = s.get('https://httpbin.org/digest-auth/auth/user/passwd',
                      auth=HTTPDigestAuth('user', 'passwd'))
            assert r.ok
            assert r.history[0].status_code == 401

        s = Session()
        with Betamax(s).use_cassette(cassette_name):
            r = s.get('https://httpbin.org/digest-auth/auth/user/passwd',
                      auth=HTTPDigestAuth('user', 'passwd'))
            assert r.json() is not None
