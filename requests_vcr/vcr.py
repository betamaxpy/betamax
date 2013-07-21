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

    Or more concisely, you can do:

    .. code::

        s = requests.Session()
        with VCR(s).use_cassette('example') as vcr:
            r = s.get('https://httpbin.org/get')

    """

    cassette_library_dir = 'vcr/cassettes'
    default_cassette_options = {
        'record_mode': 'once',
        'match_requests_on': ['method']
    }

    def __init__(self, session, cassette_library_dir=None,
                 default_cassette_options=None, adapter_args=None):
        #: Store the requests.Session object being wrapped.
        self.session = session
        #: Store the session's original adapters.
        self.http_adapters = session.adapters.copy()
        #: Create a new adapter to replace the existing ones
        self.vcr_adapter = VCRAdapter(**(adapter_args or {}))
        self.cassette_loaded = False

        self.default_cassette_options.update(default_cassette_options or {})

        # If it was passed in, use that instead.
        if cassette_library_dir:
            self.cassette_library_dir = cassette_library_dir

    def __enter__(self):
        self.session.mount('http://', self.vcr_adapter)
        self.session.mount('https://', self.vcr_adapter)
        return self

    def __exit__(self, ex_type, ex_value, ex_traceback):
        if ex_traceback is not None:
            raise ex_type, ex_value, ex_traceback

        self.vcr_adapter.close()
        for (k, v) in self.http_adapters.items():
            self.session.mount(k, v)

    def use_cassette(self, cassette_name, serialize='json'):
        """Tell VCR which cassette you wish to use for the context.

        :param str cassette_name: relative name, without the serialization
            format, of the cassette you wish VCR would use
        :param str serialize: the format you want VCR to serialize the request
            and response data to and from
        """
        def _can_load_cassette():
            # This test sucks. We may be creating the cassettes for the
            # first time. We shouldn't be doing this, but I'll leave it as
            # a reminder for later.
            if self.default_cassette_options['record_mode'] in ['once']:
                return True

            return os.path.exists(os.path.join(
                self.cassette_library_dir, '{0}.{1}'.format(
                    cassette_name, serialize
                )
            ))

        if _can_load_cassette():
            self.vcr_adapter.load_cassette(cassette_name, serialize)
        else:
            raise ValueError('Cassette must have a valid name and may not be'
                             ' None.')
        return self


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
