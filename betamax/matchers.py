from requests.compat import urlparse
matcher_registry = {}


class BaseMatcher(object):

    """
    Base class that ensures sub-classes that implement custom matchers can be
    registered and have the only method that is required.

    Usage::

        from betamax import Betamax, BaseMatcher

        class MyMatcher(BaseMatcher):
            name = 'my'

            def match(self, request, recorded_request):
                # My fancy matching algorithm

        Betamax.register_request_matcher(MyMatcher)

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
        self.on_init()

    def on_init(self):
        """Method to implement if you wish something to happen in ``__init__``.

        The return value is not checked and this is called at the end of
        ``__init__``. It is meant to provide the matcher author a way to
        perform things during initialization of the instance that would
        otherwise require them to override ``BaseMatcher.__init__``.
        """
        return None

    def match(self, request, recorded_request):
        """This is a method that must be implemented by the user.

        :param PreparedRequest request: A requests PreparedRequest object
        :param dict recorded_request: A dictionary containing the serialized
            request in the cassette
        :returns bool: True if they match else False
        """
        raise NotImplementedError('The match method must be implemented on'
                                  ' %s' % self.__class__.__name__)


class BodyMatcher(BaseMatcher):
    # Matches based on the body of the request
    name = 'body'

    def match(self, request, recorded_request):
        return request.body == recorded_request['body']


class HeadersMatcher(BaseMatcher):
    # Matches based on the headers of the request
    name = 'headers'

    def match(self, request, recorded_request):
        return dict(request.headers) == recorded_request['headers']


class HostMatcher(BaseMatcher):
    # Matches based on the host of the request
    name = 'host'

    def match(self, request, recorded_request):
        request_host = urlparse(request.url).netloc
        recorded_host = urlparse(recorded_request['uri']).netloc
        return request_host == recorded_host


class MethodMatcher(BaseMatcher):
    # Matches based on the method of the request
    name = 'method'

    def match(self, request, recorded_request):
        return request.method == recorded_request['method']


class PathMatcher(BaseMatcher):
    # Matches based on the path of the request
    name = 'path'

    def match(self, request, recorded_request):
        request_path = urlparse(request.url).path
        recorded_path = urlparse(recorded_request['uri']).path
        return request_path == recorded_path


class QueryMatcher(BaseMatcher):
    # Matches based on the query of the request
    name = 'query'

    def to_dict(self, query):
        """Turn the query string into a dictionary"""
        if not query:
            return {}
        return dict(q.split('=') for q in query.split('&'))

    def match(self, request, recorded_request):
        request_query = self.to_dict(urlparse(request.url).query)
        recorded_query = self.to_dict(
            urlparse(recorded_request['uri']).query
        )
        return request_query == recorded_query


class URIMatcher(BaseMatcher):
    # Matches based on the uri of the request
    name = 'uri'

    def on_init(self):
        # Get something we can use to match query strings with
        self.query_matcher = QueryMatcher().match

    def match(self, request, recorded_request):
        queries_match = self.query_matcher(request, recorded_request)
        request_url, recorded_url = request.url, recorded_request['uri']
        return self.all_equal(request_url, recorded_url) and queries_match

    def parse(self, uri):
        parsed = urlparse(uri)
        return {
            'scheme': parsed.scheme,
            'netloc': parsed.netloc,
            'path': parsed.path,
            'fragment': parsed.fragment
            }

    def all_equal(self, new_uri, recorded_uri):
        new_parsed = self.parse(new_uri)
        recorded_parsed = self.parse(recorded_uri)
        return (new_parsed == recorded_parsed)


_matchers = [BodyMatcher, HeadersMatcher, HostMatcher, MethodMatcher,
             PathMatcher, QueryMatcher, URIMatcher]
matcher_registry.update(dict((m.name, m()) for m in _matchers))
del _matchers
