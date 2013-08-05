import os
from requests.adapters import BaseAdapter, HTTPAdapter
from requests_vcr.cassette import Cassette


class VCRAdapter(BaseAdapter):

    """This object is an implementation detail of the library.

    It is not meant to be a public API and is not exported as such.

    """

    def __init__(self, **kwargs):
        super(VCRAdapter, self).__init__()
        self.cassette = None
        self.cassette_name = None
        self.http_adapter = HTTPAdapter(**kwargs)
        self.serialize = None
        self.options = {}

    def close(self):
        self.http_adapter.close()

    def send(self, request, stream=False, timeout=None, verify=True,
             cert=None, proxies=None):
        """
        if self.cassette:
            # load cassette
            return self.cassette.as_response()
        else:
            # store the response because if they're using us we should
            # probably be storing the cassette
            response = self.http_adapter.send(
                request, stream=stream, timeout=timeout, verify=verify,
                cert=cert, proxies=proxies
            )
            if self.cassette_name:
                Cassette.from_response(response).save(self.cassette_name)
            return response
        """
        match_on = self.config['match_requests_on']
        if (self.cassette and not self.cassette.is_empty() and
                self.cassette.match(request, match_on)):
            return self.cassette.as_response()
        else:
            response = self.http_adapter.send(
                request, stream=stream, timeout=timeout, verify=verify,
                cert=cert, proxies=proxies
                )
            self.cassette.save(response)
            return response

    def load_cassette(self, cassette_name, serialize, options):
        self.cassette_name = cassette_name
        self.serialize = serialize
        self.options.update(options)
        # load cassette into memory
        if self.cassette_exists():
            self.cassette = Cassette(cassette_name, serialize)
        elif os.path.exists(os.path.dirname(cassette_name)):
            self.cassette = Cassette(cassette_name, serialize, 'w+b')

    def cassette_exists(self):
        if self.cassette_name and os.path.exists(self.cassette_name):
            return True
        return False
