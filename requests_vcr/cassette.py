import io
import json
import mimetools
from requests.models import PreparedRequest, Response
from requests.structures import CaseInsensitiveDict
from requests.packages.urllib3 import HTTPResponse


def serialize_prepared_request(request, method):
    return {
        'body': request.body,
        'headers': dict(request.headers),
        'method': request.method,
        'url': request.url,
    }


def deserialize_prepared_request(serialized):
    p = PreparedRequest()
    p.body = serialized['body']
    p.headers = CaseInsensitiveDict(serialized['headers'])
    p.method = serialized['method']
    p.url = serialized['url']
    return p


def serialize_response(response, method):
    return {
        'content': response.content,
        'encoding': response.encoding,
        'headers': dict(response.headers),
        'status_code': response.status_code,
        'url': response.url,
    }


def deserialize_response(serialized):
    r = Response()
    r.encoding = serialized['encoding']
    r.headers = CaseInsensitiveDict(serialized['headers'])
    r.url = serialized['url']
    r.status_code = serialized['status_code']
    body = io.StringIO(serialized['content'])
    r.raw = HTTPResponse(body, status=r.status_code, headers=r.headers,
                         preload_content=False,
                         original_response=MockHTTPResponse(r.headers))
    return r


class Cassette(object):

    """The Cassette object abstracts how requests are saved.

    Example usage::

        c = Cassette('vcr/cassettes/httpbin.json', 'json', 'w+b')
        r = requests.get('https://httpbin.org/get')
        c.save(r)

    """

    def __init__(self, cassette_name, serialize, mode='rb'):
        self.cassette_name = cassette_name
        self.serialize_format = serialize
        self.recorded_response = None
        self.fd = open(cassette_name, mode)

    def serialize(self, response):
        return {
            'request': serialize_prepared_request(response.request,
                                                  self.serialize_format),
            'response': serialize_response(response, self.serialize_format),
        }

    def deserialize(self, serialized_data):
        r = deserialize_response(serialized_data['response'])
        r.request = deserialize_prepared_request(serialized_data['request'])
        return r

    def save(self, response):
        self.recorded_response = response
        serialized = self.serialize(response)
        json.dump(serialized, self.fd)
        # Flush the file so that people can inspect files immediately (if they
        # so please)
        self.fd.flush()

    def as_response(self):
        if not self.recorded_response:
            serialized = json.load(self.fd)
            self.recorded_response = self.deserialize(serialized)
        return self.recorded_response

    def is_empty(self):
        try:
            self.as_response()
        except ValueError:
            return True
        else:
            return False


class MockHTTPResponse(object):
    def __init__(self, headers):
        h = ["%s: %s" % (k, v) for (k, v) in headers.items()]
        h = io.StringIO('\r\n'.join(h))
        self.msg = mimetools.Message(h)

    def isclosed(self):
        return False
