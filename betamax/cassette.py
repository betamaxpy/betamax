import email.message
import io
import json
from datetime import datetime
from functools import partial

from betamax.matchers import matcher_registry
from requests.compat import is_py2
from requests.models import PreparedRequest, Response
from requests.packages.urllib3 import HTTPResponse
from requests.structures import CaseInsensitiveDict


def serialize_prepared_request(request, method):
    return {
        'body': request.body,
        'headers': dict(
            (coerce_content(k), v) for (k, v) in request.headers.items()
        ),
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


def coerce_content(content):
    if hasattr(content, 'decode') and not is_py2:
        return content.decode()
    return content


def serialize_response(response, method):
    return {
        'content': coerce_content(response.content),
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
    add_urllib3_response(serialized, r)
    return r


def body_io(content):
    if is_py2:
        return io.StringIO(content)
    if hasattr(content, 'encode'):
        content = content.encode()
    return io.BytesIO(content)


def add_urllib3_response(serialized, response):
    h = HTTPResponse(
        body_io(serialized['content']),
        status=response.status_code,
        headers=response.headers,
        preload_content=False,
        original_response=MockHTTPResponse(response.headers)
    )
    response.raw = h


def timestamp():
    stamp = datetime.utcnow().isoformat()
    i = stamp.rindex('.')
    return stamp[:i]


class Cassette(object):

    """The Cassette object abstracts how requests are saved.

    Example usage::

        c = Cassette('vcr/cassettes/httpbin.json', 'json', 'w+')
        r = requests.get('https://httpbin.org/get')
        c.save(r)

    """

    def __init__(self, cassette_name, serialize, mode='r'):
        self.cassette_name = cassette_name
        self.serialize_format = serialize
        self.serialized = None
        self.interactions = []
        self.match_options = set()
        self.fd = open(cassette_name, mode)
        self.load_interactions()

    def eject(self):
        self.save_cassette()
        self.fd.flush()
        self.fd.close()

    def find_match(self, request):
        opts = self.match_options
        # Curry those matchers
        matchers = [partial(matcher_registry[o].match, request) for o in opts]
        for i in self.interactions:
            if i.match(matchers):
                return i
        return None

    def is_empty(self):
        if self.interactions:
            return False
        return True

    def load_interactions(self):
        if self.serialized is None:
            self.load_serialized_data()

        if 'http_interactions' not in self.serialized:
            return

        self.interactions = [
            Interaction(i) for i in self.serialized['http_interactions']
        ]

    def load_serialized_data(self):
        if self.serialized:
            return
        try:
            self.serialized = json.load(self.fd)
        except ValueError:
            self.serialized = {}

    def save_interaction(self, response, request):
        interaction = self.serialize_interaction(response, request)
        self.serialized.setdefault('http_interactions', []).append(
            interaction
        )
        self.interactions.append(Interaction(interaction, response))

    def save_cassette(self):
        if 'w' in self.fd.mode or 'r+' in self.fd.mode:
            json.dump({
                'http_interactions': [i.json for i in self.interactions],
                'recorded_with': 'betamax',
            }, self.fd)
            # Flush the file so that people can inspect files immediately (if
            # they so please)
            self.fd.flush()

    def serialize_interaction(self, response, request):
        return {
            'request': serialize_prepared_request(request,
                                                  self.serialize_format),
            'response': serialize_response(response, self.serialize_format),
            'recorded_at': timestamp(),
        }


class Interaction(object):
    def __init__(self, interaction, response=None):
        self.json = interaction
        if response:
            self.recorded_response = response
        else:
            self.deserialize()

    def as_response(self):
        return self.recorded_response

    def deserialize(self):
        r = deserialize_response(self.json['response'])
        r.request = deserialize_prepared_request(self.json['request'])
        self.recorded_at = datetime.strptime(
            self.json['recorded_at'], '%Y-%m-%dT%H:%M:%S'
        )
        self.recorded_response = r

    def match(self, matchers):
        request = self.json['request']
        return all(m(request) for m in matchers)


class MockHTTPResponse(object):
    def __init__(self, headers):
        h = ["%s: %s" % (k, v) for (k, v) in headers.items()]
        h = io.StringIO('\r\n'.join(h) or None)
        # Thanks to Python 3, we have to use the slightly more awful API below
        # mimetools was deprecated so we have to use email.message.Message
        # which takes no arguments in its initializer.
        self.msg = email.message.Message()
        self.msg.set_payload(h)

    def isclosed(self):
        return False
