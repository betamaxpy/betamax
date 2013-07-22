from requests.adapters import BaseAdapter, HTTPAdapter


class VCRAdapter(BaseAdapter):

    """This object is an implementation detail of the library.

    It is not meant to be a public API and is not exported as such.

    """

    def __init__(self, **kwargs):
        super(VCRAdapter, self).__init__()
        self.http_adapter = HTTPAdapter(**kwargs)
        self.cassette_name = None
        self.serialize = None
        self.cassette_loaded = False

    def close(self):
        self.http_adapter.close()

    def send(self, request, stream=False, timeout=None, verify=True,
             cert=None, proxies=None):
        if self.cassette_loaded:
            # load cassette
            print("Bunnies!")
        else:
            # store the response because if they're using us we should
            # probably be storing the cassette
            return self.http_adapter.send(
                request, stream=stream, timeout=timeout, verify=verify,
                cert=cert, proxies=proxies
            )

    def load_cassette(self, cassette_name, serialize='json'):
        self.cassette_name = cassette_name
        self.serialize = serialize
        # load cassette into memory
        self.cassette_loaded = True
