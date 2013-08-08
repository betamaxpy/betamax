from requests.compat import urlparse
matcher_registry = {}


class BaseMatcher(type):

    """
    Base class that ensures sub-classes that implement custom matchers can be
    registered and have the only method that is required.

    Usage::

        from requests_vcr import VCR, alt_matchers

        class MyMatcher(alt_matchers.BaseMatcher):
            name = 'my'

            def match(self, request, recorded_request):
                # My fancy matching algorithm

        VCR.register(MyMatcher)

    The last line is absolutely necessary.

    The `match` method will be given a `requests.PreparedRequest` object and a
    dictionary. The dictionary always has the following keys:

    - url
    - method
    - body
    - headers

    """

    name = None

    def __init__(self):
        if not self.name:
            raise ValueError('Matchers require names')

    def match(self, request, recorded_request):
        raise RuntimeError('The match method must be implemented on %s' %
                           self.__class__.__name__)

    @staticmethod
    def metaclass(*bases):
        """Remove the need for ``six.with_metaclass``"""
        return BaseMatcher('BaseMatcher', bases, {})


class URIMatcher(BaseMatcher.metaclass()):
    name = 'uri'

    def match(self, request, recorded_request):
        return request.url == recorded_request['url']

matcher_registry[URIMatcher.name] = URIMatcher()


class MethodMatcher(BaseMatcher.metaclass()):
    name = 'method'

    def match(self, request, recorded_request):
        return request.method == recorded_request['method']

matcher_registry[MethodMatcher.name] = URIMatcher()


class HostMatcher(BaseMatcher.metaclass()):
    name = 'host'

    def match(self, request, recorded_request):
        request_host = urlparse(request.url).host
        recorded_host = urlparse(recorded_request['url']).host
        return request_host == recorded_host

matcher_registry[HostMatcher.name] = URIMatcher()
