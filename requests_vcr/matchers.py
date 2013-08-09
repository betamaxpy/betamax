from requests.compat import urlparse
matcher_registry = {}


class BaseMatcher(type):

    """
    Base class that ensures sub-classes that implement custom matchers can be
    registered and have the only method that is required.

    Usage::

        from requests_vcr.matchers import BaseMatcher

        class MyMatcher(BaseMatcher.metaclass()):
            name = 'my'

            def match(self, request, recorded_request):
                # My fancy matching algorithm

        MyMatcher()

    The `match` method will be given a `requests.PreparedRequest` object and a
    dictionary. The dictionary always has the following keys:

    - url
    - method
    - body
    - headers

    .. note:: The above usage ensures that your matcher will work across
        Python 2.6 - 3.3. If you're only targetting one major version of
        Python, you can simply use the appropriate metaclass declaration
        with BaseMatcher, e.g.,

        ::

            # Python 3
            class MyMatcher(metaclass=BaseMatcher):
                pass

            # Python 2
            class MyMatcher(object):
                __metaclass__ = BaseMatcher

    """

    name = None

    def __new__(cls, name, bases, attrs):
        new_cls = type.__new__(cls, name, bases, attrs)

        if 'metaclass' in attrs:
            del attrs['metaclass']

        matcher_registry[attrs.get('name')] = new_cls()
        return new_cls

    def match(self, request, recorded_request):
        raise RuntimeError('The match method must be implemented on %s' %
                           self.__class__.__name__)

    @staticmethod
    def metaclass(*bases):
        """Remove the need for ``six.with_metaclass``"""
        return BaseMatcher('BaseMatcher', bases, {})


class BodyMatcher(BaseMatcher.metaclass()):
    name = 'body'

    def match(self, request, recorded_request):
        return request.body == recorded_request['body']


class HeadersMatcher(BaseMatcher.metaclass()):
    name = 'headers'

    def match(self, request, recorded_request):
        return dict(request.headers) == recorded_request['headers']


class HostMatcher(BaseMatcher.metaclass()):
    name = 'host'

    def match(self, request, recorded_request):
        request_host = urlparse(request.url).netloc
        recorded_host = urlparse(recorded_request['url']).netloc
        return request_host == recorded_host


class MethodMatcher(BaseMatcher.metaclass()):
    name = 'method'

    def match(self, request, recorded_request):
        return request.method == recorded_request['method']


class PathMatcher(BaseMatcher.metaclass()):
    name = 'path'

    def match(self, request, recorded_request):
        request_path = urlparse(request.url).path
        recorded_path = urlparse(recorded_request['url']).path
        return request_path == recorded_path


class QueryMatcher(BaseMatcher.metaclass()):
    name = 'query'

    def match(self, request, recorded_request):
        request_query = urlparse(request.url).query
        recorded_query = urlparse(request.url).query
        return request_query == recorded_query


class URIMatcher(BaseMatcher.metaclass()):
    name = 'uri'

    def match(self, request, recorded_request):
        return request.url == recorded_request['url']


if None in matcher_registry:
    del matcher_registry[None]
