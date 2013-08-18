import os
from betamax import Betamax
from requests import Session


class TestBetamax(object):
    def test_record_once(self):
        s = Session()
        cassette_path = None
        with Betamax(s).use_cassette('test_record_once') as betamax:
            assert betamax.current_cassette.is_empty() is True
            r = s.get('http://httpbin.org/get')
            assert r.status_code == 200
            assert betamax.current_cassette.is_empty() is False
            cassette_path = betamax.current_cassette.cassette_name
        os.unlink(cassette_path)
        assert os.path.exists(cassette_path) is False
