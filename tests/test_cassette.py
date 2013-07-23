from requests_vcr import cassette
from requests.models import Response
import unittest


class TestCassetteModule(unittest.TestCase):
    def test_serialize_response(self):
        r = Response()
        assert cassette.serialize_response(r, 'json') is not None


if __name__ == '__main__':
    unittest.main()
