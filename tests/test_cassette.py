import io
import unittest
from requests_vcr import cassette
from requests.models import Response
from requests.structures import CaseInsensitiveDict


class TestCassetteModule(unittest.TestCase):
    def test_serialize_response(self):
        r = Response()
        r.status_code = 200
        r.encoding = 'utf-8'
        r.raw = RequestsBytesIO(b'foo')
        r.headers = CaseInsensitiveDict()
        r.url = 'http://example.com'
        serialized = cassette.serialize_response(r, 'json')
        assert serialized is not None
        assert serialized != {}
        assert serialized['status_code'] == 200
        assert serialized['encoding'] == 'utf-8'
        assert serialized['content'] == 'foo'
        assert serialized['headers'] == {}
        assert serialized['url'] == 'http://example.com'
        assert serialized['links'] == {}

    def test_serialize_prepared_request(self):
        serialized = cassette.serialize_prepared_request(None, 'json')
        assert serialized is not None
        assert serialized != {}


class RequestsBytesIO(io.BytesIO):
    def read(self, chunk_size, *args, **kwargs):
        return super(RequestsBytesIO, self).read(chunk_size)


if __name__ == '__main__':
    unittest.main()
