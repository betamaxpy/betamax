from betamax import Betamax, BetamaxError

from tests.integration.helper import IntegrationHelper


class TestRecordOnce(IntegrationHelper):
    def test_record_once(self):
        s = self.session
        with Betamax(s).use_cassette('test_record_once') as betamax:
            self.cassette_path = betamax.current_cassette.cassette_name
            assert betamax.current_cassette.is_empty() is True
            r = s.get('http://httpbin.org/get')
            assert r.status_code == 200
            assert betamax.current_cassette.is_empty() is True
            assert betamax.current_cassette.interactions != []

    def test_replays_response(self):
        s = self.session
        with Betamax(s).use_cassette('test_replays_response') as betamax:
            self.cassette_path = betamax.current_cassette.cassette_name
            assert betamax.current_cassette.is_empty() is True
            r0 = s.get('http://httpbin.org/get')
            assert r0.status_code == 200
            assert betamax.current_cassette.interactions != []
            assert len(betamax.current_cassette.interactions) == 1
            r1 = s.get('http://httpbin.org/get')
            assert len(betamax.current_cassette.interactions) == 1
            assert r1.status_code == 200
            assert r0.headers == r1.headers
            assert r0.content == r1.content


class TestRecordNone(IntegrationHelper):
    def test_record_none(self):
        s = self.session
        with Betamax(s) as betamax:
            # import pytest
            # pytest.set_trace()
            betamax.use_cassette('test', record='none')
            self.cassette_path = betamax.current_cassette.cassette_name
            assert betamax.current_cassette is not None
            self.assertRaises(BetamaxError, s.get, 'http://httpbin.org/get')

    def test_record_none_does_not_create_cassettes(self):
        s = self.session
        with Betamax(s) as betamax:
            self.assertRaises(ValueError, betamax.use_cassette,
                              'test_record_none', record='none')
        self.cassette_created = False


class TestRecordAll(IntegrationHelper):
    pass
