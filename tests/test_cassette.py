import os
import unittest

from requests_vcr import cassette
from requests.models import Response, Request
from requests.structures import CaseInsensitiveDict


class TestSerialization(unittest.TestCase):

    """Unittests for the serialization and deserialization functions.

    This tests:

        - deserialize_prepared_request
        - deserialize_response
        - serialize_prepared_request
        - serialize_response

    """

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
        r = cassette.deserialize_response(s)
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
        p = cassette.deserialize_prepared_request(s)
        assert p.body == 'key=value'
        assert p.headers == CaseInsensitiveDict(
            {'User-Agent': 'requests-vcr/test header'}
        )
        assert p.method == 'GET'
        assert p.url == 'http://example.com/'


class TestCassette(unittest.TestCase):
    cassette_name = 'test_cassette.json'

    def setUp(self):
        self.cassette = cassette.Cassette(
            TestCassette.cassette_name,
            'json',
            'w+b'
        )
        r = Response()
        r.status_code = 200
        r.encoding = 'utf-8'
        r.raw = cassette.RequestsBytesIO(b'foo')
        r.headers = CaseInsensitiveDict()
        r.url = 'http://example.com'
        self.response = r
        r = Request()
        r.method = 'GET'
        r.url = 'http://example.com'
        r.headers = {'User-Agent': 'requests-vcr/test header'}
        r.data = {'key': 'value'}
        self.response.request = r.prepare()
        self.json = {
            'request': {
                'body': 'key=value',
                'headers': {
                    'User-Agent': 'requests-vcr/test header',
                    'Content-Length': '9',
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                'method': 'GET',
                'url': 'http://example.com/',
            },
            'response': {
                'content': 'foo',
                'encoding': 'utf-8',
                'headers': {},
                'status_code': 200,
                'url': 'http://example.com',
            },
        }

    def tearDown(self):
        if os.path.exists(TestCassette.cassette_name):
            os.unlink(TestCassette.cassette_name)

    def test_serialize(self):
        assert self.json == self.cassette.serialize(self.response)

    def test_deserialize(self):
        r = self.cassette.deserialize(self.json)
        for attr in ['status_code', 'encoding', 'content', 'headers', 'url']:
            assert getattr(self.response, attr) == getattr(r, attr)
        actual_req = r.request
        expected_req = self.response.request
        for attr in ['method', 'url', 'headers', 'body']:
            assert getattr(expected_req, attr) == getattr(actual_req, attr)


if __name__ == '__main__':
    unittest.main()
