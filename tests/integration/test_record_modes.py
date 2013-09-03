from betamax import Betamax

from tests.integration.helper import IntegrationHelper


class TestBetamax(IntegrationHelper):
    def test_record_once(self):
        s = self.session
        with Betamax(s).use_cassette('test_record_once') as betamax:
            assert betamax.current_cassette.is_empty() is True
            r = s.get('http://httpbin.org/get')
            assert r.status_code == 200
            assert betamax.current_cassette.is_empty() is False
            self.cassette_path = betamax.current_cassette.cassette_name

    def test_replays_response(self):
        s = self.session
        with Betamax(s).use_cassette('test_replays_response') as betamax:
            assert betamax.current_cassette.is_empty() is True
            r0 = s.get('http://httpbin.org/get')
            assert r0.status_code == 200
            assert betamax.current_cassette.is_empty() is False
            r1 = s.get('http://httpbin.org/get')
            assert r1.status_code == 200
            assert r0.headers == r1.headers
            assert r0.content == r1.content
            self.cassette_path = betamax.current_cassette.cassette_name
