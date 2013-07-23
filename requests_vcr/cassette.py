from requests.models import Response


class Cassette(object):
    def __init__(self, cassette_name, serialize, mode='rb'):
        self.cassette_name = cassette_name
        self.serialize = serialize
        self.response = Response()
        self.fd = open(cassette_name, mode)
