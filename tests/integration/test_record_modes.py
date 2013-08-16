import os
from betamax import VCR
from requests import Session


class TestVCR(object):
    def test_record_once(self):
        s = Session()
        cassette_path = None
        with VCR(s).use_cassette('test_record_once') as vcr:
            assert vcr.current_cassette.is_empty() is True
            r = s.get('http://httpbin.org/get')
            assert r.status_code == 200
            assert vcr.current_cassette.is_empty() is False
            cassette_path = vcr.current_cassette.cassette_name
        os.unlink(cassette_path)
        assert os.path.exists(cassette_path) is False
