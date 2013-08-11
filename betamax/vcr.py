import os
from betamax.adapter import VCRAdapter
from betamax import matchers


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
        'match_requests_on': ['method'],
        're_record_interval': None,
    }

    def __init__(self, session, cassette_library_dir=None,
                 default_cassette_options=None, adapter_args=None):
        #: Store the requests.Session object being wrapped.
        self.session = session
        #: Store the session's original adapters.
        self.http_adapters = session.adapters.copy()
        #: Create a new adapter to replace the existing ones
        self.vcr_adapter = VCRAdapter(**(adapter_args or {}))
        #: Pass along the config options
        self.vcr_adapter.options = self.default_cassette_options

        self.default_cassette_options.update(default_cassette_options or {})

        # If it was passed in, use that instead.
        if cassette_library_dir:
            self.cassette_library_dir = cassette_library_dir

    def __enter__(self):
        self.session.mount('http://', self.vcr_adapter)
        self.session.mount('https://', self.vcr_adapter)
        return self

    def __exit__(self, *ex_args):
        # ex_args comes through as the exception type, exception value and
        # exception traceback. If any of them are not None, we should probably
        # try to raise the exception and not muffle anything.
        if any(ex_args):
            raise

        # No need to keep the cassette in memory any longer.
        self.vcr_adapter.eject_cassette()
        # On exit, we no longer wish to use our adapter and we want the
        # session to behave normally! Woooo!
        self.vcr_adapter.close()
        for (k, v) in self.http_adapters.items():
            self.session.mount(k, v)

    @property
    def current_cassette(self):
        return self.vcr_adapter.cassette

    @staticmethod
    def register_request_matcher(matcher_class):
        matchers.matcher_registry[matcher_class.name] = matcher_class()

    def use_cassette(self, cassette_name, serialize='json',
                     re_record_interval=None):
        """Tell VCR which cassette you wish to use for the context.

        :param str cassette_name: relative name, without the serialization
            format, of the cassette you wish VCR would use
        :param str serialize: the format you want VCR to serialize the request
            and response data to and from
        """
        def _can_load_cassette(name):
            # If we want to record a cassette we don't care if the file exists
            # yet
            if self.default_cassette_options['record_mode'] in ['once']:
                return True

            # Otherwise if we're only replaying responses, we should probably
            # have the cassette the user expects us to load and raise.
            return os.path.exists(name)

        cassette_name = os.path.join(
            self.cassette_library_dir, '{0}.{1}'.format(
                cassette_name, serialize
            ))
        if (_can_load_cassette(cassette_name) and
                serialize in ('json', 'yaml')):
            self.vcr_adapter.load_cassette(
                cassette_name, serialize, re_record_interval,
                self.default_cassette_options
            )
        else:
            # If we're not recording or replaying an existing cassette, we
            # should tell the user/developer that there is no cassette, only
            # Zuul
            raise ValueError('Cassette must have a valid name and may not be'
                             ' None.')
        return self
