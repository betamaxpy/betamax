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
        'body': request.body or '',
        'headers': dict(
            (coerce_content(k), v) for (k, v) in request.headers.items()
        ),
        'method': request.method,
        'uri': request.url,
    }


def deserialize_prepared_request(serialized):
    p = PreparedRequest()
    p.body = serialized['body']
    p.headers = CaseInsensitiveDict(serialized['headers'])
    p.method = serialized['method']
    p.url = serialized['uri']
    return p


def coerce_content(content):
    if hasattr(content, 'decode') and not is_py2:
        return content.decode()
    return content


def serialize_response(response, method):
    return {
        'body': coerce_content(response.content),
        'encoding': response.encoding,
        'headers': dict(response.headers),
        'status_code': response.status_code,
        'url': response.url,
    }


def deserialize_response(serialized):
    r = Response()
    r.encoding = serialized['encoding']
    r.headers = CaseInsensitiveDict(serialized['headers'])
    r.url = serialized.get('url', '')
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
        body_io(serialized['body']),
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

    default_cassette_options = {
        'record_mode': 'once',
        'match_requests_on': ['method', 'uri'],
        're_record_interval': None,
        'placeholders': []
    }

    def __init__(self, cassette_name, serialize, mode='r', placeholders=None):
        self.cassette_name = cassette_name
        self.serialize_format = serialize
        self.serialized = None
        self.interactions = []
        self.match_options = set()
        self.record_mode = Cassette.default_cassette_options['record_mode']
        self.placeholders = (placeholders or
                             Cassette.default_cassette_options['placeholders'])
        self.fd = open(cassette_name, mode)
        self.load_interactions()

    def clear(self):
        """Clears out this cassette"""
        self.interactions = []
        self.save_cassette()
        self.fd.seek(0, 0)

    @property
    def earliest_recorded_date(self):
        if self.interactions:
            i = sorted(self.interactions, key=lambda i: i.recorded_at)[0]
            return i.recorded_at
        return datetime.now()

    def eject(self):
        self.save_cassette()
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
        if self.serialized:
            return False
        return True

    def is_recording(self):
        values = {
            'none': False,
            'once': self.is_empty(),
        }
        return values.get(self.record_mode, True)

    def load_interactions(self):
        if self.serialized is None:
            self.load_serialized_data()

        if 'http_interactions' not in self.serialized:
            return

        self.interactions = [
            Interaction(i) for i in self.serialized['http_interactions']
        ]
        for i in self.interactions:
            i.replace_all(self.placeholders, ('placeholder', 'replace'))

    def load_serialized_data(self):
        if self.serialized:
            return
        try:
            self.serialized = json.load(self.fd)
        except ValueError:
            self.serialized = {}

    def save_interaction(self, response, request):
        interaction = self.serialize_interaction(response, request)
        # self.serialized.setdefault('http_interactions', []).append(
        #     interaction
        # )
        self.interactions.append(Interaction(interaction, response))

    def save_cassette(self):
        self.sanitize_interactions()
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

    def sanitize_interactions(self):
        for i in self.interactions:
            i.replace_all(self.placeholders)


class Interaction(object):
    def __init__(self, interaction, response=None):
        self.recorded_at = None
        self.json = interaction
        if response:
            self.recorded_response = response
        else:
            self.deserialize()

    def as_response(self):
        """Returns the Interaction as a Response object."""
        return self.recorded_response

    def deserialize(self):
        """Turns a serialized interaction into a Response."""
        r = deserialize_response(self.json['response'])
        r.request = deserialize_prepared_request(self.json['request'])
        self.recorded_at = datetime.strptime(
            self.json['recorded_at'], '%Y-%m-%dT%H:%M:%S'
        )
        self.recorded_response = r

    def match(self, matchers):
        """Return whether this interaction is a match."""
        request = self.json['request']
        return all(m(request) for m in matchers)

    def replace(self, text_to_replace, placeholder):
        """Replace sensitive data in this interaction."""
        self.replace_in_headers(text_to_replace, placeholder)
        self.replace_in_body(text_to_replace, placeholder)
        self.replace_in_uri(text_to_replace, placeholder)

    def replace_all(self, replacements, key_order=('replace', 'placeholder')):
        """Easy way to accept all placeholders registered."""
        (replace_key, placeholder_key) = key_order
        for r in replacements:
            self.replace(r[replace_key], r[placeholder_key])

    def replace_in_headers(self, text_to_replace, placeholder):
        for obj in ('request', 'response'):
            headers = self.json[obj]['headers']
            for k, v in list(headers.items()):
                if text_to_replace in v:
                    headers[k] = v.replace(text_to_replace, placeholder)

    def replace_in_body(self, text_to_replace, placeholder):
        for obj in ('request', 'response'):
            body = self.json[obj]['body']
            if text_to_replace in body:
                self.json[obj]['body'] = body.replace(
                    text_to_replace, placeholder
                )

    def replace_in_uri(self, text_to_replace, placeholder):
        for (obj, key) in (('request', 'uri'), ('response', 'url')):
            uri = self.json[obj][key]
            if text_to_replace in uri:
                self.json[obj][key] = uri.replace(
                    text_to_replace, placeholder
                )


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
