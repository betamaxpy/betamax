import io
import json
from requests.models import PreparedRequest, Response
from requests.structures import CaseInsensitiveDict


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
    r.raw = RequestsBytesIO(serialized['content'])
    r.encoding = serialized['encoding']
    r.headers = CaseInsensitiveDict(serialized['headers'])
    r.url = serialized['url']
    r.status_code = serialized['status_code']
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

    def as_response(self):
        if not self.recorded_response:
            serialized = json.load(self.fd)
            self.recorded_response = self.deserialize(serialized)
        return self.recorded_response


class RequestsBytesIO(io.BytesIO):
    def read(self, chunk_size, *args, **kwargs):
        return super(RequestsBytesIO, self).read(chunk_size)
