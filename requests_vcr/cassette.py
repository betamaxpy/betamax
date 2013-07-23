import json
from requests.models import Response


def serialize_prepared_request(request, method):
    pass


def serialize_response(response, method):
    pass


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
