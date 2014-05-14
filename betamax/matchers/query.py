# -*- coding: utf-8 -*-
from .base import BaseMatcher
from requests.compat import urlparse

try:
    from urlparse import parse_qs
except ImportError:
    from urllib.parse import parse_qs


class QueryMatcher(BaseMatcher):
    # Matches based on the query of the request
    name = 'query'

    def to_dict(self, query):
        """Turn the query string into a dictionary"""
        return parse_qs(query or '')  # Protect against None

    def match(self, request, recorded_request):
        request_query = self.to_dict(urlparse(request.url).query)
        recorded_query = self.to_dict(
            urlparse(recorded_request['uri']).query
        )
        return request_query == recorded_query
