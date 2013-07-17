import os
from requests.adapters import BaseAdapter, HTTPAdapter


class VCR(object):

    """This object contains the main API of the request-vcr library.

    This object is entirely a context manager so all you have to do is:

    .. code::

        s = requests.Session()
        with VCR(s) as vcr:
            vcr.use_cassette('example')
            r = s.get('https://httpbin.org/get')
    """

    def __init__(self, session, cassette_library_dir='vcr/cassettes/',
                 **adapter_args):
        self.session = session
        self.cassette_dir = cassette_library_dir
        self.http_adapters = session.adapters.copy()
        self.vcr_adapter = VCRAdapter(**adapter_args)
        self.session.mount('http://', self.vcr_adapter)
        self.session.mount('https://', self.vcr_adapter)
        self.cassette_loaded = False

    def __enter__(self):
        return self

    def __exit__(self):
        self.vcr_adapter.close()
        for (k, v) in self.http_adapters.items():
            self.session.mount(k, v)

    def use_cassette(self, cassette_name, serialize='json'):
        def _can_load_cassette(name, serialize):
            if cassette_name:
                # This test sucks. We may be creating the cassettes for the
                # first time. We shouldn't be doing this, but I'll leave it as
                # a reminder for later.
                return os.path.exists(os.path.join(
                    self.cassette_dir, '{0}.{1}'.format(name, serialize)
                ))
            return False

        if _can_load_cassette(cassette_name, serialize):
            self.vcr_adapter.load_cassette(cassette_name, serialize)
        else:
            raise ValueError('Cassette must have a valid name and may not be'
                             ' None.')


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
        self.session.adapters = self.old_adapters.copy()

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
