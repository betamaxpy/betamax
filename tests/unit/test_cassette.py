import os
import unittest
from datetime import datetime

from betamax import cassette
from requests.models import Response, Request
from requests.packages import urllib3
from requests.structures import CaseInsensitiveDict


def decode(s):
    if hasattr(s, 'decode'):
        return s.decode()
    return s


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
        r.headers = CaseInsensitiveDict()
        r.url = 'http://example.com'
        cassette.add_urllib3_response({
            'body': {
                'string': decode('foo'),
                'encoding': 'utf-8'
            }
        }, r)
        serialized = cassette.serialize_response(r, 'json')
        assert serialized is not None
        assert serialized != {}
        assert serialized['status_code'] == 200
        assert serialized['body']['encoding'] == 'utf-8'
        assert serialized['body']['string'] == 'foo'
        assert serialized['headers'] == {}
        assert serialized['url'] == 'http://example.com'

    def test_deserialize_response(self):
        s = {
            'body': {
                'string': decode('foo'),
                'encoding': 'utf-8'
            },
            'headers': {
                'Content-Type': decode('application/json')
            },
            'url': 'http://example.com/',
            'status_code': 200,
            'recorded_at': '2013-08-31T00:00:01'
        }
        r = cassette.deserialize_response(s)
        assert r.content == b'foo'
        assert r.encoding == 'utf-8'
        assert r.headers == {'Content-Type': 'application/json'}
        assert r.url == 'http://example.com/'
        assert r.status_code == 200

    def test_serialize_prepared_request(self):
        r = Request()
        r.method = 'GET'
        r.url = 'http://example.com'
        r.headers = {'User-Agent': 'betamax/test header'}
        r.data = {'key': 'value'}
        p = r.prepare()
        serialized = cassette.serialize_prepared_request(p, 'json')
        assert serialized is not None
        assert serialized != {}
        assert serialized['method'] == 'GET'
        assert serialized['uri'] == 'http://example.com/'
        assert serialized['headers'] == {
            'Content-Length': '9',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'betamax/test header',
        }
        assert serialized['body'] == 'key=value'

    def test_deserialize_prepared_request(self):
        s = {
            'body': 'key=value',
            'headers': {
                'User-Agent': 'betamax/test header',
            },
            'method': 'GET',
            'uri': 'http://example.com/',
        }
        p = cassette.deserialize_prepared_request(s)
        assert p.body == 'key=value'
        assert p.headers == CaseInsensitiveDict(
            {'User-Agent': 'betamax/test header'}
        )
        assert p.method == 'GET'
        assert p.url == 'http://example.com/'

    def test_add_urllib3_response(self):
        r = Response()
        r.status_code = 200
        r.headers = {}
        cassette.add_urllib3_response({
            'body': {
                'string': decode('foo'),
                'encoding': 'utf-8'
            }
        }, r)
        assert isinstance(r.raw, urllib3.response.HTTPResponse)
        assert r.content == b'foo'
        assert isinstance(r.raw._original_response, cassette.MockHTTPResponse)


class TestCassette(unittest.TestCase):
    cassette_name = 'test_cassette.json'

    def setUp(self):
        self.cassette = cassette.Cassette(
            TestCassette.cassette_name,
            'json',
            'w+'
        )
        r = Response()
        r.status_code = 200
        r.encoding = 'utf-8'
        r.headers = CaseInsensitiveDict({'Content-Type': decode('foo')})
        r.url = 'http://example.com'
        cassette.add_urllib3_response({
            'body': {
                'string': decode('foo'),
                'encoding': 'utf-8'
            }
        }, r)
        self.response = r
        r = Request()
        r.method = 'GET'
        r.url = 'http://example.com'
        r.headers = {}
        r.data = {'key': 'value'}
        self.response.request = r.prepare()
        self.response.request.headers.update(
            {'User-Agent': 'betamax/test header'}
        )
        self.json = {
            'request': {
                'body': 'key=value',
                'headers': {
                    'User-Agent': 'betamax/test header',
                    'Content-Length': '9',
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                'method': 'GET',
                'uri': 'http://example.com/',
            },
            'response': {
                'body': {
                    'string': decode('foo'),
                    'encoding': 'utf-8',
                },
                'headers': {'Content-Type': decode('foo')},
                'status_code': 200,
                'url': 'http://example.com',
            },
            'recorded_at': '2013-08-31T00:00:00',
        }
        self.date = datetime(2013, 8, 31)
        self.cassette.save_interaction(self.response, self.response.request)
        self.interaction = self.cassette.interactions[0]
        self.interaction.recorded_at = self.date

    def tearDown(self):
        try:
            self.cassette.eject()
        except:
            pass
        if os.path.exists(TestCassette.cassette_name):
            os.unlink(TestCassette.cassette_name)

    def test_serialize_interaction(self):
        serialized = self.cassette.serialize_interaction(
            self.response, self.response.request
        )
        assert serialized['request'] == self.json['request']
        assert serialized['response'] == self.json['response']
        assert serialized.get('recorded_at') is not None

    def test_holds_interactions(self):
        assert isinstance(self.cassette.interactions, list)
        assert self.cassette.interactions != []
        assert self.interaction in self.cassette.interactions

    def test_find_match(self):
        self.cassette.match_options = set(['uri', 'method'])
        i = self.cassette.find_match(self.response.request)
        assert i is not None
        assert self.interaction is i

    def test_eject(self):
        self.cassette.eject()
        assert self.cassette.fd.closed

    def test_earliest_recorded_date(self):
        assert self.interaction.recorded_at is not None
        assert self.cassette.earliest_recorded_date is not None


class TestInteraction(unittest.TestCase):
    def setUp(self):
        self.request = {
            'body': 'key=value&key2=secret_value',
            'headers': {
                'User-Agent': 'betamax/test header',
                'Content-Length': '9',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': '123456789abcdef',
                },
            'method': 'GET',
            'uri': 'http://example.com/',
        }
        self.response = {
            'body': {
                'string': decode('foo'),
                'encoding': 'utf-8'
            },
            'headers': {
                'Content-Type': decode('foo'),
                'Set-Cookie': 'cookie_name=cookie_value'
            },
            'status_code': 200,
            'url': 'http://example.com',
        }
        self.json = {
            'request': self.request,
            'response': self.response,
            'recorded_at': '2013-08-31T00:00:00',
        }
        self.interaction = cassette.Interaction(self.json)
        self.date = datetime(2013, 8, 31)

    def test_as_response(self):
        r = self.interaction.as_response()
        assert isinstance(r, Response)

    def test_deserialized_response(self):
        def check_uri(attr):
            # Necessary since PreparedRequests do not have a uri attr
            if attr == 'uri':
                return 'url'
            return attr
        r = self.interaction.as_response()
        for attr in ['status_code', 'headers', 'url']:
            assert self.response[attr] == decode(getattr(r, attr))
        assert self.response['body']['string'] == decode(r.content)
        actual_req = r.request
        expected_req = self.request
        for attr in ['method', 'uri', 'headers', 'body']:
            assert expected_req[attr] == getattr(actual_req, check_uri(attr))

        assert self.date == self.interaction.recorded_at

    def test_match(self):
        matchers = [lambda x: True, lambda x: False, lambda x: True]
        assert self.interaction.match(matchers) is False
        matchers[1] = lambda x: True
        assert self.interaction.match(matchers) is True

    def test_replace(self):
        self.interaction.replace('123456789abcdef', '<AUTH_TOKEN>')
        self.interaction.replace('cookie_value', '<COOKIE_VALUE>')
        self.interaction.replace('secret_value', '<SECRET_VALUE>')
        self.interaction.replace('foo', '<FOO>')
        self.interaction.replace('http://example.com', '<EXAMPLE_URI>')

        header = self.interaction.json['request']['headers']['Authorization']
        assert header == '<AUTH_TOKEN>'
        header = self.interaction.json['response']['headers']['Set-Cookie']
        assert header == 'cookie_name=<COOKIE_VALUE>'
        body = self.interaction.json['request']['body']
        assert body == 'key=value&key2=<SECRET_VALUE>'
        body = self.interaction.json['response']['body']
        assert body == {'encoding': 'utf-8', 'string': '<FOO>'}
        uri = self.interaction.json['request']['uri']
        assert uri == '<EXAMPLE_URI>/'
        uri = self.interaction.json['response']['url']
        assert uri == '<EXAMPLE_URI>'

    def test_replace_in_headers(self):
        self.interaction.replace_in_headers('123456789abcdef', '<AUTH_TOKEN>')
        self.interaction.replace_in_headers('cookie_value', '<COOKIE_VALUE>')
        header = self.interaction.json['request']['headers']['Authorization']
        assert header == '<AUTH_TOKEN>'
        header = self.interaction.json['response']['headers']['Set-Cookie']
        assert header == 'cookie_name=<COOKIE_VALUE>'

    def test_replace_in_body(self):
        self.interaction.replace_in_body('secret_value', '<SECRET_VALUE>')
        self.interaction.replace_in_body('foo', '<FOO>')
        body = self.interaction.json['request']['body']
        assert body == 'key=value&key2=<SECRET_VALUE>'
        body = self.interaction.json['response']['body']
        assert body == {'encoding': 'utf-8', 'string': '<FOO>'}

    def test_replace_in_uri(self):
        self.interaction.replace_in_uri('http://example.com', '<EXAMPLE_URI>')
        uri = self.interaction.json['request']['uri']
        assert uri == '<EXAMPLE_URI>/'
        uri = self.interaction.json['response']['url']
        assert uri == '<EXAMPLE_URI>'


class TestMockHTTPResponse(unittest.TestCase):
    def setUp(self):
        self.resp = cassette.MockHTTPResponse({
            decode('Header'): decode('value')
        })

    def test_isclosed(self):
        assert self.resp.isclosed() is False

    def test_is_Message(self):
        assert isinstance(self.resp.msg, cassette.email.message.Message)
