import unittest
from requests_vcr import cassette
from requests.models import Response, Request
from requests.structures import CaseInsensitiveDict


class TestCassetteModule(unittest.TestCase):
    def test_serialize_response(self):
        r = Response()
        r.status_code = 200
        r.encoding = 'utf-8'
        r.raw = cassette.RequestsBytesIO(b'foo')
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

    def test_deserialize_response(self):
        s = {
            'content': 'foo',
            'encoding': 'utf-8',
            'headers': {
                'Content-Type': 'application/json'
            },
            'url': 'http://example.com/',
            'status_code': 200,
        }
        r = cassette.deserialize_response(s, 'json')
        assert r.content == 'foo'
        assert r.encoding == 'utf-8'
        assert r.headers == {'Content-Type': 'application/json'}
        assert r.url == 'http://example.com/'
        assert r.status_code == 200

    def test_serialize_prepared_request(self):
        r = Request()
        r.method = 'GET'
        r.url = 'http://example.com'
        r.headers = {'User-Agent': 'requests-vcr/test header'}
        r.data = {'key': 'value'}
        p = r.prepare()
        serialized = cassette.serialize_prepared_request(p, 'json')
        assert serialized is not None
        assert serialized != {}
        assert serialized['method'] == 'GET'
        assert serialized['url'] == 'http://example.com/'
        assert serialized['headers'] == {
            'Content-Length': '9',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'requests-vcr/test header',
        }
        assert serialized['body'] == 'key=value'

    def test_deserialize_prepared_request(self):
        s = {
            'body': 'key=value',
            'headers': {
                'User-Agent': 'requests-vcr/test header',
            },
            'method': 'GET',
            'url': 'http://example.com/',
        }
        p = cassette.deserialize_prepared_request(s, 'json')
        assert p.body == 'key=value'
        assert p.headers == CaseInsensitiveDict(
            {'User-Agent': 'requests-vcr/test header'}
        )
        assert p.method == 'GET'
        assert p.url == 'http://example.com/'


if __name__ == '__main__':
    unittest.main()
