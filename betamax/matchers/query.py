# -*- coding: utf-8 -*-
from .base import BaseMatcher
from requests.compat import urlparse


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
