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


def deserialize_prepared_request(serialized, method):
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
        'headers': response.headers,
        'status_code': response.status_code,
        'url': response.url,
    }


def deserialize_response(serialized, method):
    r = Response()
    r.raw = RequestsBytesIO(serialized['content'])
    r.encoding = serialized['encoding']
    r.headers = CaseInsensitiveDict(serialized['headers'])
    r.url = serialized['url']
    r.status_code = serialized['status_code']
    return r


class Cassette(object):
    def __init__(self, cassette_name, serialize, mode='rb'):
        self.cassette_name = cassette_name
        self.serialize_format = serialize
        self.recorded_response = Response()
        self.fd = open(cassette_name, mode)

    def serialize(self, response):
        if self.serialize == 'json':
            data = {
                'request': {},
                'response': {},
            }
            json.dump(data, self.fd)


class RequestsBytesIO(io.BytesIO):
    def read(self, chunk_size, *args, **kwargs):
        return super(RequestsBytesIO, self).read(chunk_size)
